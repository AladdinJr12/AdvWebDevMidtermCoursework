import os 
import sys 
#sys module in Python provides tools to interact directly with the Python runtime environment.
import django
import csv #---For reading and writing to csv files---# 

#-----Sets up the django environment-----#
sys.path.append(os.path.join(os.getcwd(), "")) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CM3015MidtermCoursework.settings') 
django.setup()

#---importing from models.py from the covidData fodder---#
from covidData.models import *

#---Function for converting "" values----#
def convertIntoNull(dataRow):
    if dataRow == "":
        return None
    return dataRow 

#----function for converting percentage string data into their float value---#
def convertIntoFloat(value):
    #---in case the data is empty---#
    if value == "":
        return None  # Return None if the value is NaN
    try:
        return float(value.strip('%')) 
    except ValueError:
        return None  # Return None if the conversion fails

#---Function for converting "" into 0----#
def convertIntoZero(value):
    if value == "":
        return 0
    return value 

data_file = "../covid19_sg.csv"

#---Ensuring all data files are empty before hand-----#
CovidPhases.objects.all().delete()
Cases.objects.all().delete()
Vaccination.objects.all().delete()
Deaths.objects.all().delete()
HospitalizedPatients.objects.all().delete()
HospitalDischarges.objects.all().delete()
IsolationCases.objects.all().delete()

with open(data_file) as csv_file:
    csvReaderVar = csv.reader(csv_file, delimiter = ",")
    # Skipping the header row
    header = csvReaderVar.__next__()

    for row in csvReaderVar:
#-----___________Adding in data related to covid phases__________----//
        phaseRow = row[24]
        #---Correcting the data for the empty isolation phase column----#
        if row[24] == "":
            phaseRow = "Pre-isolation/Lockdown phase"
        phaseData = CovidPhases.objects.create(date = row[0],
                                               phase = phaseRow)
        # Retrieve the created or existing CovidPhases instance for foreign key use---#
        CovidPhase_instance = CovidPhases.objects.get(date=row[0])

#-----___________Adding in data related to covid cases__________----//        
        caseData = Cases.objects.create(
            date= CovidPhase_instance,
            daily_confirmed_cases = row[1],
            false_positive_cases = convertIntoNull(row[2]),
            cumulative_cases = row[3],
            daily_imported_cases = row[12],
            daily_local_transmission_cases = row[13],
            local_dorm_residence_cases = convertIntoNull(row[14]) ,
            local_non_dorm_residence_cases = convertIntoNull(row[15]), 
            linked_community_cases = convertIntoNull(row[22]),
            unlinked_community_cases = convertIntoNull(row[23]) 
        )
        
#-----___________Adding in data related to covid p__________----//   
        vaccinationData = Vaccination.objects.create(
            date = CovidPhase_instance,
            cumulative_vaccine_doses = convertIntoNull(row[25] ),
            cumulative_vaccinated_individuals = convertIntoNull(row[26]),
             cumulative_completed_vaccination_individuals = convertIntoNull(row[27]),
            percentage_of_population_who_completed_at_least_one_dose = convertIntoFloat( row[28] ),
            percentage_of_population_who_completed_vaccination = convertIntoFloat( row[29] ),
            sinovac_vaccine_doses = convertIntoNull(row[30]),
            cumulative_sinovac_vaccine_individuals = convertIntoNull(row[31]),
            doses_of_other_vaccines_recognised_by_WHO = convertIntoNull(row[32] ),
            cumulative_individuals_using_other_vaccines_recognised_by_WHO = convertIntoNull( row[33]),
            individuals_who_took_booster_shots = convertIntoNull(row[34]),   
            population_percentage_who_taken_booster_shots = convertIntoFloat(row[35])
        )

#-----___________Adding in data related to covid deaths__________----// 
        deathdata = Deaths.objects.create(
            date = CovidPhase_instance,
            daily_deaths = row[9],
            cumulative_deaths = row[10],
            non_covid_related_deaths = row[5] ,
            covid_pos_deaths = row[11]
        )

#-----___________Adding in data related to hospitalized patients__________----// 
        hospitalizedPatientsData = HospitalizedPatients.objects.create(
            date = CovidPhase_instance,
            daily_discharged_patients = row[4],
            cumulative_discharged_patients = row[6], 
            discharged_for_isolation = row[7],
            still_hospitalized_patients = row[8],
            ICU_patients = row[16],
            general_wards_patients = convertIntoNull(row[17]),
            patients_in_isolation = convertIntoZero(row[18]),
            patients_requring_oxygen_supplementation_or_unstable = convertIntoZero(row[21])
        )

#-----___________Adding in data related to hospital discharges __________----// 
        dischargesRow = HospitalDischarges.objects.create(
            date = CovidPhase_instance,
            total_hospital_discharges = convertIntoNull(row[20])
        )

#-----___________Adding in data related to isolation cases __________----// 
        isolationRow = IsolationCases.objects.create(
            date = CovidPhase_instance,
            total_completed_isolation_cases = convertIntoZero(row[19])
        )

print("The dataset rows have been added successfully!")
    





    


