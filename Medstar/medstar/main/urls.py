from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='main'),
    path('management/', hospital_management, name='management'),
    path('edit_hospital/', edit_hospital_title, name='edit_hospital'),

    path('create_doctor/', create_doctor, name='create_doctor'),
    path('edit_doctor/', edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:pk>/', delete_doctor, name='delete_doctor'),

    path('patients_view/', patients_view, name='patients_view'),
    path('edit_patient/', edit_patient, name='edit_patient'),
    path('add_patient/', add_patient, name='add_patient'),
    path('delete_patient/<int:pk>/', delete_patient, name='delete_patient'),
    path('references/', all_references, name='all_references')
]