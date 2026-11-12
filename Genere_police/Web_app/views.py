from django.conf import settings
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import JsonResponse
import httpx
import jwt
from django.contrib import messages
from auth_app.models import User
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import logging
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

def error_view(request, error_message, error_details, redirect_url):
    return render(request, 'error.html', {
        'error_message': error_message,
        'error_details': error_details,
        'redirect_url': redirect_url
    })

async def common_data_admin(cookies):

    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{settings.API_URL}/api/auth/user", cookies=cookies)
        users_response = await client.get(f"{settings.API_URL}/api/auth/listUser", cookies=cookies)
        branche_response = await client.get(f"{settings.API_URL}/api/branchType/branch", cookies=cookies)
        agence_response = await client.get(f"{settings.API_URL}/api/agence/agenceLieu", cookies=cookies)
        polices_response = await client.get(f"{settings.API_URL}/api/police/ListPolice", cookies=cookies)

        if all(response.status_code == 200 for response in [user_response, users_response, branche_response, agence_response, polices_response]):
            user_data = user_response.json()
            users_data = users_response.json()
            branches_data = branche_response.json()
            agences_data = agence_response.json()
            polices_data = polices_response.json()

            # Trier les utilisateurs par ID décroissant
            users_data = sorted(users_data, key=lambda user: user.get("id", 0), reverse=True)

            # Calculer les statistiques
            nombre_admins = sum(1 for user in users_data if user.get("role") == "admin")
            nombre_users = sum(1 for user in users_data if user.get("role") == "user")
            nombre_branches = len(branches_data)
            nombre_agences = len(agences_data)
            nombre_polices = len(polices_data)

            return {
                "user": user_data,
                "users": users_data,
                "branches": branches_data,
                "agences": agences_data,
                "polices": polices_data,
                "nombre_admins": nombre_admins,
                "nombre_users": nombre_users,
                "nombre_branches": nombre_branches,
                "nombre_agences": nombre_agences,
                "nombre_polices": nombre_polices
            }
        else:
            return None

async def authentification(request):
    agences = cache.get('agences')
    if not agences:
        try:
            async with httpx.AsyncClient() as client:
                agences_response = await client.get(f"{settings.API_URL}/api/agence/agenceLieu")
                if agences_response.status_code == 200:
                    agences = agences_response.json()
                    cache.set('agences', agences, timeout=300)
                else:
                    agences = []
                    logger.warning(f"Erreur lors de la récupération des agences : {agences_response.status_code}")
        except httpx.RequestError as e:
            agences = []
            logger.error(f"Erreur de connexion à l'API : {e}")
    return await sync_to_async(render)(request, 'authentification.html', {'agences': agences})

async def register(request):
    agences = cache.get('agences')
    if not agences:
        try:
            async with httpx.AsyncClient() as client:
                agences_response = await client.get(f"{settings.API_URL}/api/agence/agenceLieu")
                if agences_response.status_code == 200:
                    agences = agences_response.json()
                    cache.set('agences', agences, timeout=300)
                else:
                    agences = []
        except httpx.RequestError as e:
            agences = []
    
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        agence = request.POST.get('agence')
        password = request.POST.get('password')
        verif = request.POST.get('verif')

        if password != verif:
            await sync_to_async(messages.error)(request, "Les mots de passe ne correspondent pas. Réessayez.")
            return await sync_to_async(render)(request, 'authentification.html', {'email': email, 'username': username, 'agence': agence})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.API_URL}/api/auth/register",
                    json={'email': email, 'username': username, 'agence_id': agence, 'password': password}
                )
                if response.status_code == 201:
                    await sync_to_async(messages.success)(request, "Inscription réussie.")
                    return redirect('login')
                else:
                    try:
                        errors = response.json()
                    except ValueError:
                        errors = {}
                    if isinstance(errors, dict) and errors:
                        details = " | ".join(
                            f"{champ} : {' '.join(map(str, msgs)) if isinstance(msgs, list) else msgs}"
                            for champ, msgs in errors.items())
                    else:
                        details = "Inscription échouée."
                    await sync_to_async(messages.error)(request, f"Erreur : {details}")
        except httpx.RequestError as e:
            await sync_to_async(messages.error)(request, f"Erreur de connexion à l'API : {e}")
            return await sync_to_async(render)(request, 'authentification.html', {'agences': agences, 'email': email, 'username': username, 'agence': agence})
    return await sync_to_async(render)(request, 'authentification.html', {'agences': agences, 'email': email, 'username': username, 'agence': agence})

async def login(request):
    agences = cache.get('agences')
    if not agences:
        try:
            async with httpx.AsyncClient() as client:
                agences_response = await client.get(f"{settings.API_URL}/api/agence/agenceLieu")
                if agences_response.status_code == 200:
                    agences = agences_response.json()
                    cache.set('agences', agences, timeout=300)
                else:
                    agences = []
        except httpx.RequestError as e:
            agences = []
            
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            async with httpx.AsyncClient() as client:
                api_response = await client.post(
                    f"{settings.API_URL}/api/auth/login",
                    data={'email': email, 'password': password}
                )
                if api_response.status_code == 200:
                    jwt_token = api_response.json().get('jwt')
                    payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
                    role = payload.get('role')
                    response = redirect('dashboard' if role == 'admin' else 'home')
                    response.set_cookie(key='jwt', value=jwt_token, httponly=True,
                                        samesite='Lax', secure=not settings.DEBUG, max_age=3600)
                    await sync_to_async(request.session.__setitem__)('user_id', payload['id'])
                    await sync_to_async(messages.success)(request, 'Connexion réussie')
                    return response
                else:
                    await sync_to_async(messages.error)(request, 'Email ou mot de passe incorrect')
        except httpx.RequestError:
            await sync_to_async(messages.error)(request, 'Erreur de connexion avec le serveur, veuillez réessayer')
        return await sync_to_async(render)(request, 'authentification.html', {'email': email})
    return await sync_to_async(render)(request, 'authentification.html', {'agences': agences})

async def home(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Session expirée", "Votre session a expiré. Veuillez vous reconnecter.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        user = await sync_to_async(User.objects.get)(id=payload['id'])

        async with httpx.AsyncClient() as client:
            clients_response = await client.get(f"{settings.API_URL}/api/souscripteur/Listclients", cookies=request.COOKIES)
            clients = clients_response.json() if clients_response.status_code == 200 else []

            polices_response = await client.get(f"{settings.API_URL}/api/police/ListPolice", cookies=request.COOKIES)
            polices = polices_response.json() if polices_response.status_code == 200 else []
        
        nombre_clients = len(clients)
        nombre_polices = len(polices)

        return await sync_to_async(render)(request, 'home.html', {
            'user': user,
            'clients': clients,
            'polices': polices,
            'nombre_clients': nombre_clients,
            'nombre_polices': nombre_polices
        })
        
    except ExpiredSignatureError:
        return error_view(request, "Session expirée", "Votre session a expiré. Veuillez vous reconnecter.", "/web/login")
    except (InvalidTokenError, User.DoesNotExist):
        return error_view(request, "Authentification invalide", "Authentification invalide. Veuillez vous reconnecter.", "/web/login")

async def dashboard(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté en tant qu'admin pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        if payload.get('role') != 'admin':
            return error_view(request, "Accès refusé", "Vous devez être un administrateur.", "/web/login")

        user_id = await sync_to_async(request.session.get)('user_id')
        if not user_id:
            return error_view(request, "Session invalide", "Session invalide ou expirée, veuillez vous reconnecter", "/web/login")

        common_data = await common_data_admin(request.COOKIES)
        
        if common_data:
            return await sync_to_async(render)(request, "Dashboard.html", {
                "user": common_data["user"],
                "users": common_data["users"],
                "branches": common_data["branches"],
                "polices": common_data["polices"],
                "nombre_admins": common_data["nombre_admins"],
                "nombre_users": common_data["nombre_users"],
                "nombre_branches": common_data["nombre_branches"],
                "nombre_agences": common_data["nombre_agences"],
            })
        else:
            return error_view(request, "Erreur de récupération des données", "Une erreur est survenue lors de la récupération des données", "/web/login")
    except (ExpiredSignatureError, InvalidTokenError):
        return error_view(request, "Session expirée", "Session expirée ou token invalide. Veuillez vous reconnecter.", "/web/login")

async def branche(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté en tant qu'admin pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        if payload.get('role') != 'admin':
             return error_view(request, "Accès refusé", "Vous devez être un administrateur.", "/web/login")

        if request.method == 'POST':
            nom_branche = request.POST.get('nom_branche')
            prefixe = request.POST.get('prefixe')
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{settings.API_URL}/api/branchType/branch",
                        json={'nom_branche': nom_branche, 'prefixe': prefixe},
                        cookies=request.COOKIES
                    )
                    if response.status_code == 201:
                        await sync_to_async(messages.success)(request, "Branche ajoutée avec succès")
                    else:
                        await sync_to_async(messages.error)(request, "Une erreur est survenue lors de l'ajout de la branche")
            except httpx.RequestError:
                await sync_to_async(messages.error)(request, "Impossible de se connecter au serveur. Veuillez réessayer.")

        common_data = await common_data_admin(request.COOKIES)
        
        if common_data:
            return await sync_to_async(render)(request, "branche.html", {
                "user": common_data["user"],
                "branches": common_data["branches"],
                "nombre_admins": common_data["nombre_admins"],
                "nombre_users": common_data["nombre_users"],
                "nombre_branches": common_data["nombre_branches"],
                "nombre_agences": common_data["nombre_agences"],
            })
        else:
            return error_view(request, "Erreur de récupération des données", "Une erreur est survenue lors de la récupération des données", "/web/login")
    except (ExpiredSignatureError, InvalidTokenError):
        return error_view(request, "Session expirée", "Session expirée ou token invalide. Veuillez vous reconnecter.", "/web/login")

async def user(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté en tant qu'admin pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        if payload.get('role') != 'admin':
            return error_view(request, "Accès refusé", "Accès refusé : Vous devez être un administrateur.", "/web/login")

        user_id = await sync_to_async(request.session.get)('user_id')
        if not user_id:
            return error_view(request, "Session invalide", "Session invalide ou expirée, veuillez vous reconnecter", "/web/login")

        common_data = await common_data_admin(request.COOKIES)
        
        if common_data:
            user_agence_id = common_data["user"].get("agence_id")
            return await sync_to_async(render)(request, "user.html", {
                "user": common_data["user"],
                "users": common_data["users"],
                "agences": common_data["agences"],
                "user_agence_id": user_agence_id,
                "nombre_admins": common_data["nombre_admins"],
                "nombre_users": common_data["nombre_users"],
                "nombre_branches": common_data["nombre_branches"],
                "nombre_agences": common_data["nombre_agences"],
            })
        else:
            return error_view(request, "Erreur de récupération des données", "Une erreur est survenue lors de la récupération des données", "/web/login")
    except (ExpiredSignatureError, InvalidTokenError):
        return error_view(request, "Session expirée", "Session expirée ou token invalide. Veuillez vous reconnecter.", "/web/login")

async def agence(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté en tant qu'admin pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        if payload.get('role') != 'admin':
            return error_view(request, "Accès refusé", "Vous devez d'abord être connecté en tant qu'admin pour accéder à cette page.", "/web/login")

        if request.method == 'POST':
            nom_agence = request.POST.get('nom_agence')
            ville = request.POST.get('ville')
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{settings.API_URL}/api/agence/agenceLieu",
                        json={'nom_agence': nom_agence, 'ville': ville},
                        cookies=request.COOKIES
                    )
                    if response.status_code == 201:
                        await sync_to_async(messages.success)(request, "Agence ajoutée avec succès")
                    else:
                        await sync_to_async(messages.error)(request, "Une erreur est survenue lors de l'ajout de l'agence")
            except httpx.RequestError:
                await sync_to_async(messages.error)(request, "Impossible de se connecter au serveur. Veuillez réessayer.")

        common_data = await common_data_admin(request.COOKIES)
        
        if common_data:
            return await sync_to_async(render)(request, "agence.html", {
                "user": common_data["user"],
                "agences": common_data["agences"],
                "nombre_admins": common_data["nombre_admins"],
                "nombre_users": common_data["nombre_users"],
                "nombre_branches": common_data["nombre_branches"],
                "nombre_agences": common_data["nombre_agences"],
            })
        else:
            return error_view(request, "Erreur de récupération des données", "Une erreur est survenue lors de la récupération des données", "/web/login")
    except (ExpiredSignatureError, InvalidTokenError):
        return error_view(request, "Session expirée", "Session expirée ou token invalide. Veuillez vous reconnecter.", "/web/login")
    
async def client(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        user = await sync_to_async(User.objects.get)(id=payload['id'])

        async with httpx.AsyncClient() as client:
            clients_response = await client.get(f"{settings.API_URL}/api/souscripteur/Listclients", cookies=request.COOKIES)
            clients = clients_response.json() if clients_response.status_code == 200 else []

            polices_response = await client.get(f"{settings.API_URL}/api/police/ListPolice", cookies=request.COOKIES)
            polices = polices_response.json() if polices_response.status_code == 200 else []
        
        nombre_clients = len(clients)
        nombre_polices = len(polices)

        return await sync_to_async(render)(request, 'client.html', {
            'user': user,
            'clients': clients,
            'polices': polices,
            'nombre_clients': nombre_clients,
            'nombre_polices': nombre_polices
        })

    except ExpiredSignatureError:
        return error_view(request, "Session expirée", "Session expirée. Veuillez vous reconnecter.", "/web/login")
    except (InvalidTokenError, User.DoesNotExist):
        return error_view(request, "Authentification invalide", "Authentification invalide. Veuillez vous reconnecter.", "/web/login")
    
async def searchClient(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        search_term = request.GET.get('q', '').strip()

        async with httpx.AsyncClient() as client:
            clients_response = await client.get(
                f"{settings.API_URL}/api/souscripteur/Listclients", 
                cookies=request.COOKIES
            )
            
            if clients_response.status_code != 200:
                return JsonResponse({'error': 'Failed to fetch clients'}, status=500)
                
            clients = clients_response.json()
            
            if search_term:
                filtered_clients = [
                    client for client in clients 
                    if search_term.lower() in client.get('num_compte_client', '').lower()
                ]
                return JsonResponse(filtered_clients, safe=False)
                
            return JsonResponse([], safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

async def police_assurance(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        user = await sync_to_async(User.objects.get)(id=payload['id'])

        async with httpx.AsyncClient() as client:
            branches_response = await client.get(f"{settings.API_URL}/api/branchType/branch", cookies=request.COOKIES)
            branches = branches_response.json() if branches_response.status_code == 200 else []

            polices_response = await client.get(f"{settings.API_URL}/api/police/ListPolice", cookies=request.COOKIES)
            polices = polices_response.json() if polices_response.status_code == 200 else []
            
            clients_response = await client.get(f"{settings.API_URL}/api/souscripteur/Listclients", cookies=request.COOKIES)
            clients = clients_response.json() if clients_response.status_code == 200 else []

        nombre_clients = len(clients)
        nombre_polices = len(polices)

        return await sync_to_async(render)(request, 'Police_assurance.html', {
            'user': user,
            'branches': branches,
            'polices': polices,
            'nombre_clients': nombre_clients,
            'nombre_polices': nombre_polices
        })

    except ExpiredSignatureError:
        return error_view(request, "Session expirée", "Session expirée. Veuillez vous reconnecter.", "/web/login")
    except (InvalidTokenError, User.DoesNotExist):
        return error_view(request, "Authentification invalide", "Authentification invalide. Veuillez vous reconnecter.", "/web/login")
    
async def historique(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return error_view(request, "Accès refusé", "Vous devez d'abord être connecté pour accéder à cette page.", "/web/login")

    try:
        payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
        user = await sync_to_async(User.objects.get)(id=payload['id'])

        async with httpx.AsyncClient() as client:
            polices_response = await client.get(f"{settings.API_URL}/api/police/ListPolice", cookies=request.COOKIES)
            polices = polices_response.json() if polices_response.status_code == 200 else []
            
            clients_response = await client.get(f"{settings.API_URL}/api/souscripteur/Listclients", cookies=request.COOKIES)
            clients = clients_response.json() if clients_response.status_code == 200 else []
            
        nombre_clients = len(clients)
        nombre_polices = len(polices)

        return await sync_to_async(render)(request, 'historique.html', {
            'user': user,
            'polices': polices,
            'nombre_clients': nombre_clients,
            'nombre_polices': nombre_polices
        })

    except ExpiredSignatureError:
        return error_view(request, "Session expirée", "Session expirée. Veuillez vous reconnecter.", "/web/login")
    except (InvalidTokenError, User.DoesNotExist):
        return error_view(request, "Authentification invalide", "Authentification invalide. Veuillez vous reconnecter.", "/web/login")

def logout(request):
    response = redirect('login')
    response.delete_cookie('jwt')
    request.session.flush()
    messages.success(request, "Déconnexion réussie")
    return response