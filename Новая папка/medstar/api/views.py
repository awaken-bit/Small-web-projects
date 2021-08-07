from main.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from django.db.models import *

import datetime
import string
import random


class DoctorInfo(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})
    
    def post(self, request):
        user = request.user
        if user.is_authenticated and request.user.doctor.is_director:
            speks = request.data
            try:
                doctor = user.doctor.hospital.doctor_set.get(user_id=int(speks.get('id')))
            except:
                return Response({'messange':'Ошибка в данных.'})

            return Response({"message": 'Success', "data": serializers.DoctorSerializer(doctor).data})
        else:
            return Response({'messange':'Пользователь не авторизован.'})

class DoctorsInDepartments(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})
    
    def post(self, request):
        user = request.user
        if user.is_authenticated and request.user.doctor.is_director:
            speks = request.data
            if speks.get('id') == 'all':
                department = request.user.doctor.hospital
            else:
                try:
                    department = user.doctor.hospital.department_set.get(id=int(speks.get('id')))
                except:
                    return Response({'messange':'Ошибка в данных.'})
            
            return Response({"message": 'Success', 
                            "data": serializers.DoctorSerializer(department.doctor_set.order_by('-user_id').all(), 
                                                                many=True).data})

class CreatePassword(APIView):
    def get(self, request):
        chars = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
        password = ''.join([random.choice(random.choice(chars)) for i in range(15)])

        return Response({'password': password})

class SearchPatients(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        speks = request.data
        try:
            speks['name']
        except:
            return Response({"message": 'Ошибка в данных'})

        patients = request.user.doctor.hospital.patient_set.order_by('-id').all()
        patients = patients.filter(last_name__istartswith = speks['name'])

        return Response({"message": 'Success',
                        "data": serializers.PatientSerializer(patients, many=True).data})

class SearchDoctors(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        speks = request.data
        try:
            speks['name']
        except:
            return Response({"message": 'Ошибка в данных'})

        doctors = request.user.doctor.hospital.doctor_set.order_by('-user_id').all()
        doctors = doctors.filter(user__last_name__istartswith = speks['name'])

        return Response({"message": 'Success',
                        "data": serializers.DoctorSerializer(doctors, many=True).data})

class PatientInfo(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        speks = request.data
        user = request.user
        try:
            patient = user.doctor.hospital.patient_set.get(id = int(speks.get('id')))
        except:
            return Response({"message": 'Нет такого пациента'})

        return Response({"message": 'Success',
                        "data": serializers.PatientSerializer(patient).data}) 