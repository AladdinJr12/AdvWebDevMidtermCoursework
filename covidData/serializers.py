from rest_framework import serializers
from .models import *

class CovidPhasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidPhases
        fields = '__all__'  # Include all fields from the model

class CasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cases
        fields = '__all__'

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = '__all__'

class DeathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deaths
        fields = '__all__'

class HospitalizedPatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalizedPatients
        fields = '__all__'

class HospitalDischargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDischarges
        fields = '__all__'

class IsolationCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsolationCases
        fields = '__all__'



