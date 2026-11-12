from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status

from police_app.views import JWTAuthenticationPermission
from .models import Clients
from .serializers import ClientSerializer

class ClientListView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    @swagger_auto_schema(
        operation_description="Récupérer la liste des clients",
        responses={200: ClientSerializer(many=True)},
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
        clients = Clients.objects.all().order_by('-date_creation')
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SearchClientView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    @swagger_auto_schema(
        operation_description="Rechercher un client par son numéro de compte",
        manual_parameters=[
            openapi.Parameter(
                'num_compte_client',
                openapi.IN_QUERY,
                description="Numéro de compte du client",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token JWT (Format: Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ClientSerializer(), 404: "Client non trouvé"}
    )
    def get(self, request):
        num_compte_client = request.query_params.get("num_compte_client")

        if num_compte_client:
            try:
                client = Clients.objects.get(num_compte_client=num_compte_client)
                serializer = ClientSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Clients.DoesNotExist:
                return Response({"erreur": "Client non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            clients = Clients.objects.all().order_by('-date_creation')
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class AddClientView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    @swagger_auto_schema(
        operation_description="Créer un nouveau client",
        request_body=ClientSerializer,
        responses={201: ClientSerializer(), 400: "Données invalides"},
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
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClientView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    @swagger_auto_schema(
        operation_description="Récupérer un client par ID",
        responses={200: ClientSerializer(), 404: "Client non trouvé"},
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
    def get(self, request, pk):
        if pk:
            try:
                client = Clients.objects.get(pk=pk)
                serializer = ClientSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Clients.DoesNotExist:
                return Response({"erreur": "Client non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        clients = Clients.objects.all().order_by('-date_creation')
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Mettre à jour un client par ID",
        request_body=ClientSerializer,
        responses={200: ClientSerializer(), 404: "Client non trouvé"},
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
    def put(self, request, pk):
        if not pk:
            return Response({"erreur": "ID du client requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Clients.objects.get(pk=pk)
        except Clients.DoesNotExist:
            return Response({"erreur": "Client non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientSerializer(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Supprimer un client par ID",
        responses={204: "Client supprimé avec succès", 404: "Client non trouvé"},
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
    def delete(self, request, pk):
        if not pk:
            return Response({"erreur": "ID du client requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Clients.objects.get(pk=pk)
        except Clients.DoesNotExist:
            return Response({"erreur": "Client non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        client.delete()
        return Response({"message": "Client supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
