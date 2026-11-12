from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from police_app.views import JWTAuthenticationPermission
from .models import Branche_assurance
from .serializers import Branche_Serializer

class BranchListCreateView(ListCreateAPIView):
    queryset = Branche_assurance.objects.all().order_by('id')
    serializer_class = Branche_Serializer
    permission_classes = [JWTAuthenticationPermission]

    @swagger_auto_schema(
        operation_description="Récupérer la liste des branches",
        responses={200: Branche_Serializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Créer une nouvelle branche",
        request_body=Branche_Serializer,
        responses={201: Branche_Serializer(), 400: "Données invalides"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BranchDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Branche_assurance.objects.all()
    serializer_class = Branche_Serializer
    permission_classes = [JWTAuthenticationPermission]

    @swagger_auto_schema(
        operation_description="Récupérer une branche par ID",
        responses={200: Branche_Serializer(), 404: "Branche introuvable"},
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID de la branche",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Mettre à jour une branche par ID",
        request_body=Branche_Serializer,
        responses={200: Branche_Serializer(), 404: "Branche introuvable"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Supprimer une branche par ID",
        responses={204: "Branche supprimée avec succès", 404: "Branche introuvable"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
