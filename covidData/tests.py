from django.test import TestCase
#--Importing the factories and models---#
from covidData.factories import *
from covidData.models import *
from django.urls import reverse


# Create your tests here.
#--________Checking that the factories are working_________--#
class FactoriesTestCase(TestCase):
    def test_create_covid_phase(self):
        # Use the factory to create a CovidPhase
        covid_phase = CovidPhasesFactory.create()
        #----Check that a CovidPhase object is created---#
        self.assertIsInstance(covid_phase, CovidPhases)
        self.assertIsNotNone(covid_phase.date)
        self.assertIsNotNone(covid_phase.phase)
    
    # Use the factory to create a Cases model and check if its created--#
    def test_create_cases(self):
        cases = CasesFactory.create()
        self.assertIsInstance(cases, Cases)
        self.assertIsNotNone(cases.date)
        self.assertIsNotNone(cases.daily_confirmed_cases)
        self.assertIsNotNone(cases.false_positive_cases)
        self.assertIsNotNone(cases.cumulative_cases)
        self.assertIsNotNone(cases.daily_imported_cases)
        self.assertIsNotNone(cases.daily_local_transmission_cases)
        self.assertIsNotNone(cases.local_dorm_residence_cases)
        self.assertIsNotNone(cases.local_non_dorm_residence_cases)
        self.assertIsNotNone(cases.linked_community_cases)
        self.assertIsNotNone(cases.unlinked_community_cases)

     # Use the factory to create a Vaccination model and check if its created--#
    def test_create_vaccination(self):
        vaccination = VaccinationFactory.create()
        self.assertIsInstance(vaccination, Vaccination)
        self.assertIsNotNone(vaccination.date)
        self.assertIsNotNone(vaccination.cumulative_vaccine_doses)
        self.assertIsNotNone(vaccination.cumulative_vaccinated_individuals)
        self.assertIsNotNone(vaccination.cumulative_completed_vaccination_individuals)
        self.assertIsNotNone(vaccination.percentage_of_population_who_completed_at_least_one_dose)
        self.assertIsNotNone(vaccination.percentage_of_population_who_completed_vaccination)
        self.assertIsNotNone(vaccination.sinovac_vaccine_doses)
        self.assertIsNotNone(vaccination.cumulative_sinovac_vaccine_individuals)
        self.assertIsNotNone(vaccination.doses_of_other_vaccines_recognised_by_WHO)
        self.assertIsNotNone(vaccination.cumulative_individuals_using_other_vaccines_recognised_by_WHO)
        self.assertIsNotNone(vaccination.individuals_who_took_booster_shots)
        self.assertIsNotNone(vaccination.population_percentage_who_taken_booster_shots)

    # Use the factory to create a Deaths model and check if its created--#
    def test_create_deaths(self):
        death = DeathsFactory.create()
        self.assertIsInstance(death, Deaths)
        self.assertIsNotNone(death.date)
        self.assertIsNotNone(death.daily_deaths)
        self.assertIsNotNone(death.cumulative_deaths)
        self.assertIsNotNone(death.non_covid_related_deaths)
        self.assertIsNotNone(death.covid_pos_deaths)

    def test_create_hospitalized_patients(self):
        hospitalized_patients = HospitalizedPatientsFactory.create()
        self.assertIsInstance(hospitalized_patients, HospitalizedPatients)
        self.assertIsNotNone(hospitalized_patients.date)
        self.assertIsNotNone(hospitalized_patients.daily_discharged_patients)
        self.assertIsNotNone(hospitalized_patients.cumulative_discharged_patients)
        self.assertIsNotNone(hospitalized_patients.discharged_for_isolation)
        self.assertIsNotNone(hospitalized_patients.still_hospitalized_patients)
        self.assertIsNotNone(hospitalized_patients.ICU_patients)
        self.assertIsNotNone(hospitalized_patients.general_wards_patients)
        self.assertIsNotNone(hospitalized_patients.patients_in_isolation)
        self.assertIsNotNone(hospitalized_patients.patients_requring_oxygen_supplementation_or_unstable)


    def test_create_hospital_discharges(self):
        hospital_discharges = HospitalDischargesFactory.create()
        self.assertIsInstance(hospital_discharges, HospitalDischarges)
        self.assertIsNotNone(hospital_discharges.date)
        self.assertIsNotNone(hospital_discharges.total_hospital_discharges)

    def test_create_isolation_cases(self):
        isolation_cases = IsolationCasesFactory.create()
        self.assertIsInstance(isolation_cases, IsolationCases)
        self.assertIsNotNone(isolation_cases.date)
        self.assertIsNotNone(isolation_cases.total_completed_isolation_cases)

#______testing the functions/classes created in views.py/which in turn test for urls.py___________#
class IndexViewTests(TestCase):
    #----Checking the index function from views.py is working correctly
    def test_index_with_data(self):
        covidPhase1 = CovidPhasesFactory.create(date="2022-01-01")
        covidPhase2 = CovidPhasesFactory.create(date="2022-12-31")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        #---index from views.py returns a date range from earliest recorded date to latest--#
        #--This just checks if index is working---#
        self.assertContains(response, "01 January 2022 - 31 December 2022")
    
    def test_index_no_data(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        #---index from views.py returns a string notifying no date range when no data iss available--#
        #--This just checks if index is working---#
        self.assertContains(response, "No date range available")

#_____________Note this retreives data over selected date range___________#
class DynamicModelListViewTests(TestCase):
    def setUp(self):
        #----Create some sample data----#
        covidPhase1 = CovidPhasesFactory.create(date="2022-01-01")
        covidPhase2 = CovidPhasesFactory.create(date="2022-01-02")
        covidPhase3 = CovidPhasesFactory.create(date="2022-01-15")
        HospitalDischarge1 = HospitalDischargesFactory.create(date=covidPhase1)
        HospitalDischarge2 = HospitalDischargesFactory.create(date=covidPhase2)

    def test_valid_query_with_data(self):
        response = self.client.get(reverse('dynamic_data', kwargs={
            'data_type': 'Covid Phases', 'start_date': '2022-01-01', 'end_date': '2022-01-15'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2022-01-01")
        self.assertContains(response, "2022-01-15")

        #---Checks that the correct data_type is added in---#
        self.assertEqual(response.context['data_type'], 'Covid Phases')

        #---Checks that the retreived fieldNames are correct---#
        field_names = [field.verbose_name for field in CovidPhases._meta.fields]
        self.assertEqual(response.context['field_names'], field_names)

        #--Checks that the correct number of CovidPhases results are returned which is 3 in this case--#
        self.assertTrue(len(response.context['results']) == 3)

    def test_valid_discharges_query_with_data(self):
        response = self.client.get(reverse('dynamic_data', kwargs={
            'data_type': 'Hospital Discharges', 'start_date': '2022-01-01', 'end_date': '2022-01-15'
        }))
        self.assertEqual(response.status_code, 200)
    #--Checks that the correct number of Hospital Discharges results are returned which is 2 in this case--#
        self.assertTrue(len(response.context['results']) == 2)

    def test_invalid_data_type(self):
        response = self.client.get(reverse('dynamic_data', kwargs={
            'data_type': 'InvalidType', 'start_date': '2022-01-01', 'end_date': '2022-01-31'
        }))
        #-----Checking that it returned and invalid status_code---#
        self.assertEqual(response.status_code, 400)
        #---decoding the bytes of the error message---#
        decodedMessage = response.content.decode('utf-8')
        self.assertEqual(decodedMessage, "Invalid data type.") 


#_____testing the data for indvidual date sections (aka datapage.html/DynamicModelDetailView section)___#
class DynamicModelDetailViewTests(TestCase):
    def setUp(self):
        covidPhase1 = CovidPhasesFactory.create(date="2022-01-01")

    #----Testing that we can retreive the CovidPhase we just created---#
    def test_valid_query(self):
        response = self.client.get(reverse('individual_data', kwargs={
            'data_type': 'Covid Phases', 'selected_date': '2022-01-01'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2022-01-01")

    #----Testing that we can reject invalid data types---#
    def test_invalid_data_type(self):
        response = self.client.get(reverse('individual_data', kwargs={
            'data_type': 'InvalidType', 'selected_date': '2022-01-01'
        }))
        self.assertEqual(response.status_code, 400)

    #---Checks that it sends to noResults when no matching data entries are found--#
    def test_object_not_found(self):
        response = self.client.get(reverse('individual_data', kwargs={
            'data_type': 'Covid Phases', 'selected_date': '2023-01-01'
        }))
        self.assertRedirects(response, reverse('noResults'))

#_____________Note this creates a data entry for a selected data______________#
class DynamicModelCreateViewTests(TestCase):
    #---Testing that the form submission works when the data fields are correct--#
    def test_valid_form_submission(self):
        response = self.client.post(reverse('add-data', kwargs={
            'data_type': 'Covid Phases', 'selected_date': '2022-01-01'
        }), data={'field_name': 'value'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        #----Here the date input is incorrect since Covid doesn't exists yet---#
        response = self.client.post(reverse('add-data', kwargs={
            'data_type': 'Covid Phases', 'selected_date': '2012-01-01'
        }), data={'wrong_field': 'value'})
        self.assertEqual(response.status_code, 400)

#_____________Note this deletes a data entry based on the selected date______________#
class DynamicModelDeleteViewTests(TestCase):
    def setUp(self):
        covidPhase1 = CovidPhasesFactory.create(date="2022-01-01")
    
    def test_delete_valid_object(self):
        response = self.client.delete(reverse('delete-data', kwargs={
            'data_type': 'Covid Phases', 'date': '2022-01-01'
        }))
        self.assertEqual(response.status_code, 302)


# from .factories import HospitalizedPatientsFactory

# class DynamicModelListViewRelatedDataTests(TestCase):
#     def setUp(self):
#         phase = CovidPhasesFactory(date="2022-01-01")
#         HospitalizedPatientsFactory.create_batch(10, covid_phase=phase)

#     def test_related_data_query(self):
#         response = self.client.get(reverse('datapage_list', kwargs={
#             'data_type': 'Hospitalized Patients', 'start_date': '2022-01-01', 'end_date': '2022-01-31'
#         }))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['results']), 10)
