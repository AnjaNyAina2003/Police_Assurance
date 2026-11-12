from rest_framework import serializers
from .models import Police_assurance
from django.utils import timezone

class PoliceAssuranceSerializer(serializers.ModelSerializer):
    num_compte_client = serializers.CharField(source='num_compte_client.num_compte_client', read_only=True)
    branche_nom = serializers.CharField(source='id_branche.nom_branche', read_only=True)
    user_nom = serializers.CharField(source='id_user.username', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    client_nom = serializers.CharField(source='num_compte_client.nom_client', read_only=True)
    client_prenom = serializers.CharField(source='num_compte_client.prenom_client', read_only=True)
    date_generation = serializers.SerializerMethodField()
    date_expiration = serializers.SerializerMethodField()
    
    def get_date_generation(self, obj):
        if obj.date_generation:
            return timezone.localtime(obj.date_generation).strftime("%d/%m/%Y %H:%M")
        return None
    
    def get_date_expiration(self, obj):
        if obj.date_expiration:
            return timezone.localtime(obj.date_expiration).strftime("%d/%m/%Y %H:%M")
        return None

    class Meta:
        model = Police_assurance
        fields = ['id', 'num_police', 'num_compte_client', 'date_generation', 'agence_nom', 'user_nom', 'branche_nom', 'client_nom', 'client_prenom', 'duree_couverture', 'status', 'date_expiration']
