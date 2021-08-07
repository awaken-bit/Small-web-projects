from django.urls import path
from .views import *


urlpatterns = [
    path('create_password/', CreatePassword.as_view(), name='create_password'),

    path('doctor_info/', DoctorInfo.as_view(), name='doctor_info'),
    path('patient_info/', PatientInfo.as_view(), name='patient_info'),
    
    path('doctors_in_departments/', DoctorsInDepartments.as_view(), name='doctors_in_departments'),

    path('search_patients/', SearchPatients.as_view(), name='search_patients'),
    path('search_doctors/', SearchDoctors.as_view(), name='search_doctors')
]