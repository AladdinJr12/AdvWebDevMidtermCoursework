from django import forms
from django.forms import ModelForm
from .models import *

class CovidPhasesForm(forms.ModelForm):
    class Meta:
        model = CovidPhases
        fields = "__all__"

class CasesForm(forms.ModelForm):
    class Meta:
        model = Cases
        fields = '__all__'

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'

class DeathsForm(forms.ModelForm):
    class Meta:
        model = Deaths
        fields = '__all__'

class HospitalizedPatientsForm(forms.ModelForm):
    class Meta:
        model = HospitalizedPatients
        fields = '__all__'

class HospitalDischargesForm(forms.ModelForm):
    class Meta:
        model = HospitalDischarges
        fields = '__all__'

class IsolationCasesForm(forms.ModelForm):
    class Meta:
        model = IsolationCases
        fields = '__all__'