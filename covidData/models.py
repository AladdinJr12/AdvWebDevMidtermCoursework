from django.db import models

# Create your models here.

class CovidPhases(models.Model):
    date = models.DateField(primary_key=True)
    phase = models.TextField(null=True)

    class Meta:
            verbose_name = "CovidPhase"
            verbose_name_plural = "CovidPhases"

    def __str__(self):
        return f"{self.date}: {self.phase}"

class Cases(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    daily_confirmed_cases = models.IntegerField(null=True)
    false_positive_cases = models.IntegerField(null=True)
    cumulative_cases = models.IntegerField(null=True)
    daily_imported_cases = models.IntegerField(null=True)
    daily_local_transmission_cases = models.IntegerField(null=True)
    local_dorm_residence_cases = models.IntegerField(null=True)
    local_non_dorm_residence_cases = models.IntegerField(null=True)
    linked_community_cases = models.IntegerField(null=True)
    unlinked_community_cases = models.IntegerField(null=True)

    class Meta:
            verbose_name = "Cases"
            verbose_name_plural = "Cases"

    def __str__(self):
        return f"Covid cases on {self.date}"

class Vaccination(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    cumulative_vaccine_doses = models.IntegerField(null=True)
    cumulative_vaccinated_individuals = models.IntegerField(null=True)
    cumulative_completed_vaccination_individuals = models.IntegerField(null=True)
    percentage_of_population_who_completed_at_least_one_dose = models.FloatField(null=True)
    percentage_of_population_who_completed_vaccination = models.FloatField(null=True)
    sinovac_vaccine_doses = models.IntegerField(null=True)
    cumulative_sinovac_vaccine_individuals = models.IntegerField(null=True)
    doses_of_other_vaccines_recognised_by_WHO = models.IntegerField(null=True)
    cumulative_individuals_using_other_vaccines_recognised_by_WHO = models.IntegerField(null=True)
    individuals_who_took_booster_shots = models.IntegerField(null=True)
    population_percentage_who_taken_booster_shots = models.FloatField(null=True)

    class Meta:
        verbose_name = "Vaccination"
        verbose_name_plural = "Vaccination"

    def __str__(self):
        return f"Vaccination data on {self.date}"

class Deaths(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    daily_deaths = models.IntegerField(null=True)
    cumulative_deaths = models.IntegerField(null=True)
    non_covid_related_deaths = models.IntegerField(null=True)
    covid_pos_deaths = models.IntegerField(null=True)

    class Meta:
            verbose_name = "Deaths"
            verbose_name_plural = "Deaths"

    def __str__(self):
        return f"Death data on {self.date}"


class HospitalizedPatients(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    daily_discharged_patients = models.IntegerField(null=True)
    cumulative_discharged_patients = models.IntegerField(null=True)
    discharged_for_isolation = models.IntegerField(null=True)
    still_hospitalized_patients = models.IntegerField(null=True)
    ICU_patients = models.IntegerField(null=True)
    general_wards_patients = models.IntegerField(null=True)
    patients_in_isolation = models.IntegerField(null=True)
    patients_requring_oxygen_supplementation_or_unstable = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Hospitalized Patients"
        verbose_name_plural = "Hospitalized Patients"

    def __str__(self):
        return f"Hospitalized Patients data on {self.date}"

class HospitalDischarges(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    total_hospital_discharges = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Hospital Discharges"
        verbose_name_plural = "Hospital Discharges"

    def __str__(self):
        return f"Hospital Discharges data on {self.date}"


class IsolationCases(models.Model):
    date = models.OneToOneField(CovidPhases, on_delete=models.CASCADE, primary_key=True)
    total_completed_isolation_cases = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Isolation Cases"
        verbose_name_plural = "Isolation Cases"

    def __str__(self):
        return f"Isolation Cases data on {self.date}"


