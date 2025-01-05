from django.urls import include, path
from . import views #--Importing from views.py--//
from . import api   #Importing from api.py---//
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path ('', views.index, name='index' ),
    #--returns a selected data type over the selected date range---#
    path('dataList/<str:data_type>/<str:start_date>/<str:end_date>/', views.DynamicModelListView.as_view(), name='dynamic_data'),
    #--returns a selected data type over a selected date---#
    path('data/<str:data_type>/<str:selected_date>/', views.DynamicModelDetailView.as_view(), name="individual_data" ),
    path('add-data/<str:data_type>/<str:selected_date>/', views.DynamicModelCreateView.as_view(), name="add-data"),
    path('create-covidphase/<str:date>/<str:data_type>/', views.create_covidphase, name='create_covidphase'),
    path('delete-data/<str:date>/<str:data_type>/', views.DynamicModelDeleteView.as_view(), name='delete-data'),
    path('no-results/', views.no_results, name='noResults')
] 


