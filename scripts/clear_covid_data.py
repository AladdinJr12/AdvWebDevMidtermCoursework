#---This simply clears all of the database tables' data entries---#
#----This is so that we can show off insert_covid_data.py for the video demonstration---#


#-----Sets up the django environment-----#
import os 
import sys 
import django
sys.path.append(os.path.join(os.getcwd(), "")) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CM3015MidtermCoursework.settings') 
django.setup()

#---importing from models.py from the covidData fodder---#
from covidData.models import *

#---Ensuring all data files are empty-----#
Cases.objects.all().delete()
Vaccination.objects.all().delete()
Deaths.objects.all().delete()
HospitalizedPatients.objects.all().delete()
HospitalDischarges.objects.all().delete()
IsolationCases.objects.all().delete()
CovidPhases.objects.all().delete()

print("The database's tables' data entries have all been deleted!")