from rest_framework import serializers
from .models import Agence_assurance

class Agence_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Agence_assurance
        fields = ['id', 'nom_agence', 'ville']
        
    def create(self, validated_data):
        return Agence_assurance.objects.create(**validated_data)