#----Default import---#
from django.shortcuts import render
#-----importing the database tables/models---#
from .models import *
#--Importing the serializers---#
from .serializers import * 
#---Importing the forms---#
from .forms import *
#----Importing the different Views---#
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView

#--importing the other libraries---#
from django.http import HttpResponseBadRequest
from django.apps import apps
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

#----Map data type to model names---
MODEL_MAPPING = {
    'Covid Phases': 'CovidPhases',
    'Cases': 'Cases',
    'Hospitalized Patients': 'HospitalizedPatients',
    'Deaths': 'Deaths',
    'Vaccination': 'Vaccination',
    'Hospital Discharges': 'HospitalDischarges',
    'Isolation Cases': 'IsolationCases',
}

SERIALIZER_MODEL_MAPPING = {
    "Covid Phases": (CovidPhases, CovidPhasesSerializer),
    "Cases": (Cases, CasesSerializer),
    "Vaccination": (Vaccination, VaccinationSerializer),
    "Deaths": (Deaths, DeathsSerializer),
    "Hospitalized Patients": (HospitalizedPatients, HospitalizedPatientsSerializer),
    "Hospital Discharges": (HospitalDischarges, HospitalDischargesSerializer),
    "Isolation Cases": (IsolationCases, IsolationCasesSerializer),
}

FORMS_MODEL_MAPPiNG = {
    "Covid Phases": (CovidPhases, CovidPhasesForm),
    "Cases": (Cases, CasesForm),
    "Vaccination": (Vaccination, VaccinationForm),
    "Deaths": (Deaths, DeathsForm),
    "Hospitalized Patients": (HospitalizedPatients, HospitalizedPatientsForm),
    "Hospital Discharges": (HospitalDischarges, HospitalDischargesForm),
    "Isolation Cases": (IsolationCases, IsolationCasesForm),
}

# Create your views here.
def index(request, date_range=None):
    # Retrieve the first and last recorded dates
    first_record = CovidPhases.objects.order_by('date').first()
    last_record = CovidPhases.objects.order_by('date').last()


    if first_record and last_record:
        date_range = f"{first_record.date.strftime('%d %B %Y')} - {last_record.date.strftime('%d %B %Y')}"
        last_date_record = last_record.date.strftime('%Y-%m-%d')
    else:
        date_range = "No date range available"  #--Default date range--#
        last_date_record = "2022-01-08" #--failsafe in case it doesnt work---#

    return render(request, "covidData/homepage.html", {
        'date_range': date_range,
        'last_date_record': last_date_record
    })

#----for when the user wants to visit data for over a specific date range----#
class DynamicModelListView(ListView):
    template_name = 'covidData/datapageList.html'
    context_object_name = 'results'  # The list of results to pass to the template
    
    def get_queryset(self):
        # Get the data_type from the URL
        data_type = self.kwargs['data_type']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        # Getting the model name from the mapping
        model_name = MODEL_MAPPING.get(data_type)
     
        # Checks that the model name input is correct---//
        if not model_name:
            return HttpResponseBadRequest("Invalid data type.")

        #----Dynamically getting the corresponding model---//
        try:
            model = apps.get_model('covidData', model_name)  

        except LookupError:
            return HttpResponseBadRequest("Model not found.")

        # Query the model for data within the specified date range
        try:
            return model.objects.filter(
                date__gte=start_date,
                date__lte=end_date
            )
        except Exception as e:
            return HttpResponseBadRequest(f"Error querying the database: {e}")

    def get_context_data(self, **kwargs):
        # If an HttpResponseBadRequest was returned from get_queryset, do not proceed with context rendering
        # if isinstance(self.get_queryset(), HttpResponseBadRequest):
        #     return self.get_queryset()

        context = super().get_context_data(**kwargs)

        # --Processing the selected dates--#
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        date_range = f"{start_date} - {end_date}"

        # Get the dynamic model within this method
        data_type = self.kwargs['data_type']
        model_name = MODEL_MAPPING.get(data_type)

        #---Checks that the model name input is correct---//
        if not model_name:
            self.error_message = "Invalid data type."
            # context['error_message'] = "Invalid data type."
            self.response_status_code = 400
            #---Returning context with an error message---#
            return context

        try:
            model = apps.get_model('covidData', model_name)  # Dynamically get the model again
        
        except LookupError:
            self.error_message = "Model not found"
            # context['error_message'] = "Model not found."
            self.response_status_code = 400
            #---Returning context with an error message---#
            return context

        # For storing the resulting values----#
        processed_results = []

        # Iterate through the queryset and turn each record into a dictionary of its field names and values
        for record in self.get_queryset():
            record_data = {}
            for field in model._meta.fields:
                field_name = field.name
                record_data[field_name] = getattr(record, field_name)  # Access field values dynamically
            processed_results.append(record_data)

    #______Passing back the context aka data used in the html----# 
        #---Passing the processed/returned searched data--------#
        context['results'] = processed_results
        #---Note that verbos_name removes the '_' symbol, which needs to be added in templatetags for dict search--#
        context['field_names'] = [field.verbose_name for field in model._meta.fields]

        context['data_type'] = data_type
        context['date_range'] = date_range

        return context
    
    #----This is created to return a 400 status when test.py inserts wrong data--#
    def dispatch(self, request, *args, **kwargs):
        # Check for invalid data_type and model lookup before continuing
        data_type = self.kwargs['data_type']
        model_name = MODEL_MAPPING.get(data_type)

        if not model_name:
            return HttpResponseBadRequest("Invalid data type.")  # Return error immediately

        try:
            self.model = apps.get_model('covidData', model_name)
        except LookupError:
            return HttpResponseBadRequest("Model not found.")  # Return error immediately

        return super().dispatch(request, *args, **kwargs)
    
#----___________for when the user wants to visit data for a specific date____________----#
class DynamicModelDetailView(DetailView):
    template_name = "covidData/datapage.html"  # Template to render data
    context_object_name = "data"    # Context name for the template

    def get_object(self):
        # Extract parameters from URL
        data_type = self.kwargs['data_type']
        selected_date = self.kwargs['selected_date']

        #----Get the corresponding model and serializer dynamically----#
        model, serializer_class = SERIALIZER_MODEL_MAPPING.get(data_type, (None, None))
        if model is None or serializer_class is None:
            return HttpResponseBadRequest(f"Invalid data type: {data_type}")

        #---Try to fetch the object for the given date---#
        try:
            obj = model.objects.get(date=selected_date)
        except model.DoesNotExist:
            return None
           
        #----Serialize the data---#
        serializer = serializer_class(obj)
        #-----Save serialized data for JSON response if needed-------#
        self.serialized_data = serializer.data  
        return obj
    
    #---For when the nothing is found from the search query---#
    def dispatch(self, request, *args, **kwargs):
        #_______This is created to return a 400 status when test.py inserts wrong data________#
        data_type = self.kwargs['data_type']
        # Check for invalid data_type and model lookup before continuing
        model_name = MODEL_MAPPING.get(data_type)

        if not model_name:
            return HttpResponseBadRequest("Invalid data type.")  # Return error immediately

        try:
            self.model = apps.get_model('covidData', model_name)
        except LookupError:
            return HttpResponseBadRequest("Model not found.")  # Return error immediately
        # ________End of section that checks for when bad/incorrect data is inserted_____//

        # Call get_object first to check if the object exists
        obj = self.get_object()

        # If no object is found, redirect to the no-results page
        if obj is None:
            return redirect('noResults')
        # If object is found, proceed as usual
        return super().dispatch(request, *args, **kwargs)
    
    #---This is add in the date range and selected data type to display on the html
    def get_context_data(self, **kwargs):
        # Call the base implementation to get the default context
        context = super().get_context_data(**kwargs)
        # Add custom context variables
        context['data_type'] = self.kwargs['data_type']  # Pass data_type to template
        context['date_range'] = self.kwargs['selected_date']  # Pass selected_date to template
        return context

    def render_to_response(self, context, **response_kwargs):
        # Check if JSON response is requested
        if self.request.headers.get("Accept") == "application/json":
            return JsonResponse(self.serialized_data, safe=False)
        return super().render_to_response(context, **response_kwargs)
    
#----for Creating data for selected data type-----#    
class DynamicModelCreateView(CreateView):
    template_name = "covidData/addData.html"

    def get(self, request, *args, **kwargs):
        data_type = self.kwargs['data_type']
        selected_date = self.kwargs['selected_date']
        

        #----getting the selected model + corresponding form----#
        model, form_class = FORMS_MODEL_MAPPiNG.get(data_type, (None, None))

        if model is None or form_class is None:
            return HttpResponseBadRequest(f"Invalid data type: {data_type}")

        self.model = model
        self.form_class = form_class

        if selected_date:

            try:            
                self.covid_phase = CovidPhases.objects.get(date=selected_date)
    
            #-----When covidPhase does not exists--------#
            except CovidPhases.DoesNotExist:
                #---Redirect to the page where the user can create a CovidPhase---#
                return redirect(reverse('create_covidphase', kwargs={'date': selected_date, 'data_type': data_type}))
            
        else:
            self.covid_phase = None

        #--- Create an empty instance of the selected model ---
        self.object = model()  # Set object to an empty instance of the model

        #---This next two lines are to pass in the selected model/data_type---#
        context = self.get_context_data(*args, **kwargs)
        context['data_type'] = data_type 
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data_type = kwargs.get('data_type')
        selected_date = self.kwargs['selected_date']

        #---converting the selected date into the date format--#
        converted_selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        #---Earliest Recorded covid case in singapore----#
        reference_date = datetime(2020, 1, 20).date()

        #---For rejecting invalid date inputs---//
        if(converted_selected_date < reference_date):
            return HttpResponseBadRequest(f"Invalid date input: {selected_date}")

        #----getting the selected model + corresponding form----#
        model, form_class = FORMS_MODEL_MAPPiNG.get(data_type, (None, None))

        if model is None or form_class is None:
            return HttpResponseBadRequest(f"Invalid data type: {data_type}")

        self.model = model
        self.form_class = form_class

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        #---Redirects to homepage after successful form submission---#
        return reverse_lazy('index')  
    
    #----This is created to return a 400 status when test.py inserts wrong data--#
    def dispatch(self, request, *args, **kwargs):
        # ---heck for invalid data_type and model lookup--#
        data_type = self.kwargs['data_type']
        model_name = MODEL_MAPPING.get(data_type)

        if not model_name:
            return HttpResponseBadRequest("Invalid data type.")  #--Returns the error immediately--#

        try:
            self.model = apps.get_model('covidData', model_name)
        except LookupError:
            return HttpResponseBadRequest("Model not found.")  #--Returns the error immediately--#

        return super().dispatch(request, *args, **kwargs)

#----For adding in a data entry for CovidPhase table/mode-----#
def create_covidphase(request, date, data_type):
    if request.method == 'POST':
        form = CovidPhasesForm(request.POST)
        if form.is_valid():
            # -- saving the data -- #
            covid_phase = form.save(commit=False)
            covid_phase.date = date
            covid_phase.save()
            #---Redirecting back to the addData.html with the previously selected arguments---#
            return redirect('add-data', data_type=data_type, selected_date=date)
      
    # -- Giving them the form -- #
    else:
        form = CovidPhasesForm()

    return render(request, 'covidData/createCovidPhase.html', {'form': form, 'date': date})


class DynamicModelDeleteView(DeleteView):
    template_name = "covidData/confirmDeletePage.html"  # Optional: a confirmation template
    #---Dynamically determine the queryset based on the `data_type`----#
    def get_queryset(self):
        data_type = self.kwargs['data_type']
        model = FORMS_MODEL_MAPPiNG.get(data_type, (None, None))[0]  #---Get the model---#

        if not model:
            raise HttpResponseBadRequest(f"Invalid data type: {data_type}")

        #----Filter the queryset to search for the given `date` entry----#
        return model.objects.filter(date=self.kwargs['date'])

    def get_object(self, queryset=None):
        #---Get the specific object to delete.----#
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def get_context_data(self, **kwargs):
        #----So that we can return the selected data type + date--# 
        context = super().get_context_data(**kwargs)

        #----Get the data_type and date from kwargs--#
        data_type = self.kwargs['data_type']
        date_range = self.kwargs['date'] 

        #---Add the data_type and date_range to the context---#
        context['data_type'] = data_type
        context['date_range'] = date_range
        return context

    def get_success_url(self):
        #---Redirect to the index after successful deletion.---#
        return reverse_lazy('index')

#---This function is just for when the searched query returns nothing and it brings them to noResults.html--#
def no_results(request):
    return render(request, 'covidData/noResults.html')