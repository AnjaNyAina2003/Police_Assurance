from rest_framework import serializers
from .models import Clients
from django.utils import timezone

class ClientSerializer(serializers.ModelSerializer):
    date_creation = serializers.SerializerMethodField()

    class Meta:
        model = Clients
        fields = ['id', 'num_compte_client', 'nom_client', 'prenom_client', 'telephone', 'adresse', 'date_creation']
        
    def get_date_creation(self, obj):
        if obj.date_creation:
            return timezone.localtime(obj.date_creation).strftime("%d/%m/%Y %H:%M")
        return None