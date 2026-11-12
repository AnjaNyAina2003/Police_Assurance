from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from police_app.views import JWTAuthenticationPermission
from police_app.models import Police_assurance
from .models import Quittance
from .serializers import QuittanceSerializer
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GenerateQuittanceView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    
    @swagger_auto_schema(
        operation_description="Générer une quittance pour une police d'assurance existante",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'num_police': openapi.Schema(type=openapi.TYPE_STRING, description="Numéro de la police d'assurance")
            },
            required=['num_police']
        ),
        responses={
            201: QuittanceSerializer(),
            400: openapi.Response(description="Numéro de police requis"),
            404: openapi.Response(description="Police d'assurance introuvable")
        }
    )

    def post(self, request):
        num_police = request.data.get("num_police")

        if not num_police:
            return Response({"erreur": "Numéro de police requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            police = Police_assurance.objects.get(num_police=num_police)
        except Police_assurance.DoesNotExist:
            return Response({"erreur": "Police d'assurance introuvable"}, status=status.HTTP_404_NOT_FOUND)

        quittance = Quittance.objects.create(police_assurance=police)
        serializer = QuittanceSerializer(quittance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListQuittanceView(APIView):
    permission_classes = [JWTAuthenticationPermission]
    
    @swagger_auto_schema(
        operation_description="Lister toutes les quittances",
        responses={
            200: QuittanceSerializer(many=True)
        }
    )

    def get(self, request):
        quittances = Quittance.objects.all().order_by('-date_creation')
        serializer = QuittanceSerializer(quittances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)