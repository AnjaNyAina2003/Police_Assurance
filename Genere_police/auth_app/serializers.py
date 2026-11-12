from rest_framework import serializers

from agence_app.models import Agence_assurance
from .models import User

class User_Serializer(serializers.ModelSerializer):
    agence = serializers.CharField(source='agence.nom_agence', read_only=True)
    agence_id = serializers.PrimaryKeyRelatedField(queryset=Agence_assurance.objects.all(), source='agence', allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'agence_id','agence','password', 'role', "photo"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'role': {'read_only': True},
            'photo': {'required': False}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = 'user'
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)  # Hashage du mot de passe
            instance.save()
        return instance
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Le mot de passe doit contenir au moins 8 caractères')
        return value