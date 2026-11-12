import logging
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import BasePermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User

from .serializers import User_Serializer
import jwt, datetime

from police_app.views import JWTAuthenticationPermission

logger = logging.getLogger(__name__)

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Utilisateur non authentifié')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload['id']  
            request.user_role = payload['role']  
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session expirée, veuillez vous reconnecter')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token invalide, veuillez vous reconnecter')

        if request.user_role != 'admin': 
            raise PermissionDenied("Accès refusé : Vous devez être un administrateur")

        return True

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Créer un nouvel utilisateur",
        request_body=User_Serializer,
        responses={201: User_Serializer(), 400: "Données invalides"}
    )
    def post(self, request):
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Connexion utilisateur",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email de l'utilisateur"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Mot de passe")
            }
        ),
        responses={200: "Connexion réussie", 401: "Échec de connexion"}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email and not password:
            raise AuthenticationFailed('Email et Mot de passe requis')
        elif not email:
            raise AuthenticationFailed('Email requis')
        elif not password:
            raise AuthenticationFailed('Mot de passe requis')

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Email ou mot de passe incorrect')
 
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True, 
                            samesite='Lax', secure= not settings.DEBUG, max_age=3600)
        response.data = ({
            'message': 'Connexion reussie',
            'jwt': token
        })
        
        return response
    
class GetUserView(APIView):
    permission_classes = [IsAdminPermission]
    @swagger_auto_schema(
        operation_description="Récupérer les informations de l'utilisateur connecté",
        responses={
            200: User_Serializer(),
            401: "Utilisateur non authentifié",
            403: "Accès refusé",
            404: "Utilisateur non trouvé"
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token JWT (Format: Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Utilisateur non authentifié')
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session expirée, veuillez vous reconnecter')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token invalide, veuillez vous reconnecter')
        
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('Utilisateur non trouvé')
        
        serializer = User_Serializer(user)
        return Response(serializer.data)

class UserView(APIView):
    permission_classes = [IsAdminPermission]
    @swagger_auto_schema(
        operation_description="Récupérer un utilisateur par ID",
        responses={200: User_Serializer(), 404: "Utilisateur non trouvé"}
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        serializer = User_Serializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Mettre à jour un utilisateur par ID",
        request_body=User_Serializer,
        responses={200: User_Serializer(), 404: "Utilisateur non trouvé"}
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        serializer = User_Serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Supprimer un utilisateur par ID",
        responses={204: "Utilisateur supprimé avec succès", 404: "Utilisateur non trouvé"}
    )
    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'Utilisateur supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
    
class ListUsersView(APIView):
    permission_classes = [IsAdminPermission]
    @swagger_auto_schema(
        operation_description="Lister tous les utilisateurs",
        responses={200: User_Serializer(many=True)}
    )
    def get(self, request):
        users = User.objects.all().order_by('id')
        serializer = User_Serializer(users, many=True)
        return Response(serializer.data)
    
class UploadUserPhotoView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    
    def post(self, request, pk):
        if request.user_id != pk and request.user_role != 'admin':
            raise PermissionDenied("Accès refusé")
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username')
        photo = request.FILES.get('photo') 
        
        if username:
            user.username = username

        if photo:
            user.photo = photo
        
        try:
            user.save()
            return Response({
                'status': 'success',
                'message': 'Profil modifié avec succès'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erreur lors de la modification du profil: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)    

class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="Déconnexion de l'utilisateur",
        responses={200: "Déconnexion réussie"}
    )
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Déconnexion reussie'
        }
        
        return response