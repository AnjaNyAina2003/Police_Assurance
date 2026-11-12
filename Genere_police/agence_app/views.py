from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from auth_app.views import IsAdminPermission

from .models import Agence_assurance

from .serializers import Agence_Serializer

class AgenceListCreateView(ListCreateAPIView):
    queryset = Agence_assurance.objects.all().order_by('id')
    serializer_class = Agence_Serializer
    
    def get_permissions(self):
        if getattr(self.request, 'method', None) == 'GET':
            return [AllowAny()]
        return [IsAdminPermission()]

    @swagger_auto_schema(
        operation_description="Récupérer la liste des agences",
        responses={200: Agence_Serializer(many=True)}
    )
    def get(self, request):
        agences = Agence_assurance.objects.all().order_by('id')
        serializer = Agence_Serializer(agences, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Créer une nouvelle agence",
        request_body=Agence_Serializer,
        responses={201: Agence_Serializer(), 400: "Données invalides"}
    )
    def post(self, request):
        serializer = Agence_Serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AgenceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Agence_assurance.objects.all()
    serializer_class = Agence_Serializer
    permission_classes = [IsAdminPermission]

    @swagger_auto_schema(
        operation_description="Récupérer une agence par ID",
        responses={200: Agence_Serializer(), 404: "Agence introuvable"},
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID de l'agence",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Mettre à jour une agence par ID",
        request_body=Agence_Serializer,
        responses={200: Agence_Serializer(), 404: "Agence introuvable"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Supprimer une agence par ID",
        responses={204: "Agence supprimée avec succès", 404: "Agence introuvable"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
