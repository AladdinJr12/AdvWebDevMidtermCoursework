from django.contrib import admin

#---Added lines------#
from .models import *

# Register your models here.
class CovidPhasesAdmin(admin.ModelAdmin):
    list_display = ('date', 'phase')  # Display all relevant fields for this model
    search_fields = ('phase',)  # Search by phase
    list_filter = ('phase',)

# Admin for Cases
class CasesAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'daily_confirmed_cases',
        'false_positive_cases',
        'cumulative_cases',
        'daily_imported_cases',
        'daily_local_transmission_cases',
        'local_dorm_residence_cases',
        'local_non_dorm_residence_cases',
        'linked_community_cases',
        'unlinked_community_cases',
    )
    search_fields = ('daily_confirmed_cases', 'cumulative_cases')
    list_filter = ('daily_confirmed_cases', 'daily_imported_cases')

# Admin for Vaccination
class VaccinationAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'cumulative_vaccine_doses',
        'cumulative_vaccinated_individuals',
        'cumulative_completed_vaccination_individuals',
        'percentage_of_population_who_completed_at_least_one_dose',
        'percentage_of_population_who_completed_vaccination',
        'sinovac_vaccine_doses',
        'cumulative_sinovac_vaccine_individuals',
        'doses_of_other_vaccines_recognised_by_WHO',
        'cumulative_individuals_using_other_vaccines_recognised_by_WHO',
        'individuals_who_took_booster_shots',
        'population_percentage_who_taken_booster_shots',
    )
    search_fields = ('cumulative_vaccine_doses', 'cumulative_vaccinated_individuals')
    list_filter = ('percentage_of_population_who_completed_vaccination',)

# Admin for Deaths
class DeathsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'daily_deaths',
        'cumulative_deaths',
        'non_covid_related_deaths',
        'covid_pos_deaths',
    )
    search_fields = ('daily_deaths', 'cumulative_deaths')
    list_filter = ('daily_deaths',)

# Admin for HospitalizedPatients
class HospitalizedPatientsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'daily_discharged_patients',
        'cumulative_discharged_patients',
        'discharged_for_isolation',
        'still_hospitalized_patients',
        'ICU_patients',
        'general_wards_patients',
        'patients_in_isolation',
        'patients_requring_oxygen_supplementation_or_unstable',
    )
    search_fields = ('daily_discharged_patients', 'ICU_patients')
    list_filter = ('still_hospitalized_patients',)

# Admin for HospitalDischarges
class HospitalDischargesAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_hospital_discharges')
    search_fields = ('total_hospital_discharges',)

# Admin for IsolationCases
class IsolationCasesAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_completed_isolation_cases')
    search_fields = ('total_completed_isolation_cases',)


#-//----registering the classes----//
admin.site.register(CovidPhases, CovidPhasesAdmin)
admin.site.register(Cases, CasesAdmin)
admin.site.register(Vaccination, VaccinationAdmin)
admin.site.register(Deaths, DeathsAdmin)
admin.site.register(HospitalizedPatients, HospitalizedPatientsAdmin)
admin.site.register(HospitalDischarges, HospitalDischargesAdmin)
admin.site.register(IsolationCases, IsolationCasesAdmin)

