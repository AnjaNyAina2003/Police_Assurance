from rest_framework import serializers
from .models import Branche_assurance

class Branche_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Branche_assurance
        fields = ['id', 'nom_branche', 'prefixe']
        
    def create(self, validated_data):
        return Branche_assurance.objects.create(**validated_data)