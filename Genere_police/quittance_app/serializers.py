from rest_framework import serializers
from police_app.serializers import PoliceAssuranceSerializer
from .models import Quittance

class QuittanceSerializer(serializers.ModelSerializer):
    date_creation = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    police_assurance = PoliceAssuranceSerializer(read_only=True)

    class Meta:
        model = Quittance
        fields = ['id', 'num_quittance', 'police_assurance', 'date_creation']