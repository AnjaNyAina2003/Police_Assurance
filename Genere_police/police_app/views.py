from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from auth_app.models import User
from branch_app.models import Branche_assurance
from client_app.models import Clients

from .models import Police_assurance
from .serializers import PoliceAssuranceSerializer

class JWTAuthenticationPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Utilisateur non authentifié')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload['id']
            request.user_role = payload.get('role')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session expirée, veuillez vous reconnecter')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token invalide, veuillez vous reconnecter')

        return True
class Genere_policeView(APIView):
    permission_classes = [JWTAuthenticationPermission]

    @swagger_auto_schema(
        operation_description="Générer une nouvelle police d'assurance",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["branche_id", "num_compte_client", "duree_couverture"],
            properties={
                "branche_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID de la branche d'assurance"
                ),
                "num_compte_client": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Numéro de compte du client"
                ),
                "duree_couverture": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Durée de couverture en mois"
                )
            }
        ),
        responses={
            201: PoliceAssuranceSerializer(),
            400: "Données invalides ou informations manquantes",
            404: "Utilisateur, branche ou client non trouvé"
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
    def post(self, request):
        try:
            user = User.objects.get(id=request.user_id)
        except User.DoesNotExist:
            return Response({"erreur": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        branche_id = request.data.get("branche_id")
        num_compte_client = request.data.get("num_compte_client")
        duree_couv = request.data.get("duree_couverture")
        
        if not branche_id or not num_compte_client:
            return Response({"erreur": "Id branche et numéro de compte client requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            branche = Branche_assurance.objects.get(id=branche_id)
            client = Clients.objects.get(num_compte_client=num_compte_client)
        except Branche_assurance.DoesNotExist:
            return Response({"erreur": "Branche introuvable"}, status=status.HTTP_400_BAD_REQUEST)
        except Clients.DoesNotExist:
            return Response({"erreur": "Client introuvable"}, status=status.HTTP_400_BAD_REQUEST)
        
        if duree_couv is None:
            return Response({"erreur": "Durée de couverture requise"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            duree_couv_int = int(duree_couv)
            if duree_couv_int <= 0:
                return Response({"erreur": "La durée de couverture doit être positive"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"erreur": "Durée de couverture doit être un nombre entier valide"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        police_assurance = Police_assurance.objects.create(
            num_compte_client=client,
            agence=user.agence,
            id_user=user,
            id_branche=branche,
            duree_couverture=duree_couv_int,
            status='actif'
        )
        
        serializer = PoliceAssuranceSerializer(police_assurance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class List_policeView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    @swagger_auto_schema(
        operation_description="Récupérer la liste de toutes les polices d'assurance",
        responses={200: PoliceAssuranceSerializer(many=True)},
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
        Police_assurance.objects.filter(
            status='actif', date_expiration__lt=timezone.now()
        ).update(status='expiree')
        polices = Police_assurance.objects.all().order_by('-date_generation')
        
        serializer = PoliceAssuranceSerializer(polices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)