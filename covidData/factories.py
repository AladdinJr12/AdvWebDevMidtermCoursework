#----Factories for testing purposes---#
import factory
#---importing the models----#
from .models import *
from faker import Faker

#----For generating random data---#
fake = Faker()

class CovidPhasesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CovidPhases

    #-----Generating the fake/testing data-------#
    date = factory.Faker('date')
    #--A short description for the phase---#
    phase = factory.Faker('sentence', nb_words=5) 
    
class CasesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cases 

   #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)  #----Foreign key linking to CovidPhases---#
    daily_confirmed_cases = factory.Faker('random_int', min=0, max=5000)
    false_positive_cases = factory.Faker('random_int', min=0, max=100)
    cumulative_cases = factory.Faker('random_int', min=0, max=500000)
    daily_imported_cases = factory.Faker('random_int', min=0, max=500)
    daily_local_transmission_cases = factory.Faker('random_int', min=0, max=4500)
    local_dorm_residence_cases = factory.Faker('random_int', min=0, max=1000)
    local_non_dorm_residence_cases = factory.Faker('random_int', min=0, max=1000)
    linked_community_cases = factory.Faker('random_int', min=0, max=3000)
    unlinked_community_cases = factory.Faker('random_int', min=0, max=500)


class VaccinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vaccination

    #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)
    cumulative_vaccine_doses = factory.Faker('random_int', min=0, max=1000000)
    cumulative_vaccinated_individuals = factory.Faker('random_int', min=0, max=1000000)
    cumulative_completed_vaccination_individuals = factory.Faker('random_int', min=0, max=1000000)
    percentage_of_population_who_completed_at_least_one_dose = factory.Faker('pyfloat', min_value=0, max_value=100)
    percentage_of_population_who_completed_vaccination = factory.Faker('pyfloat', min_value=0, max_value=100)
    sinovac_vaccine_doses = factory.Faker('random_int', min=0, max=1000000)
    cumulative_sinovac_vaccine_individuals = factory.Faker('random_int', min=0, max=1000000)
    doses_of_other_vaccines_recognised_by_WHO = factory.Faker('random_int', min=0, max=1000000)
    cumulative_individuals_using_other_vaccines_recognised_by_WHO = factory.Faker('random_int', min=0, max=1000000)
    individuals_who_took_booster_shots = factory.Faker('random_int', min=0, max=1000000)
    population_percentage_who_taken_booster_shots = factory.Faker('pyfloat', min_value=0, max_value=100)


class DeathsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Deaths

    #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)
    daily_deaths = factory.Faker('random_int', min=0, max=500)
    cumulative_deaths = factory.Faker('random_int', min=0, max=100000)
    non_covid_related_deaths = factory.Faker('random_int', min=0, max=500)
    covid_pos_deaths = factory.Faker('random_int', min=0, max=500)

class HospitalizedPatientsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HospitalizedPatients

    #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)
    daily_discharged_patients = factory.Faker('random_int', min=0, max=1000)
    cumulative_discharged_patients = factory.Faker('random_int', min=0, max=100000)
    discharged_for_isolation = factory.Faker('random_int', min=0, max=1000)
    still_hospitalized_patients = factory.Faker('random_int', min=0, max=10000)
    ICU_patients = factory.Faker('random_int', min=0, max=500)
    general_wards_patients = factory.Faker('random_int', min=0, max=5000)
    patients_in_isolation = factory.Faker('random_int', min=0, max=5000)
    patients_requring_oxygen_supplementation_or_unstable = factory.Faker('random_int', min=0, max=500)


class HospitalDischargesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HospitalDischarges

    #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)
    total_hospital_discharges = factory.Faker('random_int', min=0, max=100000)


class IsolationCasesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IsolationCases

    #-----Generating the fake/testing data-------#
    date = factory.SubFactory(CovidPhasesFactory)
    total_completed_isolation_cases = factory.Faker('random_int', min=0, max=100000)