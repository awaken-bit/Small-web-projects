import datetime
from medstar.settings import MY_TIME_ZONE
from main.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from django.db.models import *

import string
import random


class DoctorInfo(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                doctor = user.doctor.hospital.doctor_set.get(user_id=int(speks.get('id')))
            except:
                return Response({'messange':'Ошибка в данных.'})

            return Response({"message": 'Success', "data": serializers.DoctorSerializer(doctor).data if user.doctor.is_director
                            else serializers.DoctorSerializerForDoctors(doctor).data})


class DoctorsInDepartments(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            if speks.get('id') == 'all':
                department = request.user.doctor.hospital
            else:
                try:
                    department = user.doctor.hospital.department_set.get(id=int(speks.get('id')))
                except:
                    return Response({'messange':'Ошибка в данных.'})
            
            return Response({"message": 'Success', 
                            "data": serializers.DoctorSerializer(department.doctor_set.order_by('-user_id').all(), many=True).data if user.doctor.is_director
                            else serializers.DoctorSerializerForDoctors(department.doctor_set.order_by('-user_id').all(), many=True).data})

class CreatePassword(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.doctor.is_director:
            chars = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
            password = ''.join([random.choice(random.choice(chars)) for i in range(15)])

            return Response({'password': password})


class SearchDoctors(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                speks['name']
            except:
                return Response({"message": 'Ошибка в данных'})

            doctors = request.user.doctor.hospital.doctor_set.order_by('-user_id').all()
            doctors = doctors.filter(user__last_name__startswith = speks['name'])
            print(doctors)

            return Response({"message": 'Success',
                            "data": serializers.DoctorSerializer(doctors, many=True).data if user.doctor.is_director 
                            else serializers.DoctorSerializerForDoctors(doctors, many=True).data})

class SearchPatients(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                speks['name']
            except:
                return Response({"message": 'Ошибка в данных'})

            patients = request.user.doctor.hospital.patient_set.order_by('-id').all()
            patients = patients.filter(last_name__istartswith = speks['name'])

            return Response({"message": 'Success',
                            "data": serializers.PatientSerializer(patients, many=True).data})

class PatientInfo(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                patient = user.doctor.hospital.patient_set.get(id = int(speks.get('id')))
            except:
                return Response({"message": 'Нет такого пациента'})

            return Response({"message": 'Success',
                            "data": serializers.PatientSerializer(patient).data})

class DoctorAppointments(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                speks['date']
                doctor = user.doctor.hospital.doctor_set.get(id=int(speks['id']))
            except:
                return Response({"message": 'Нет такого доктора или даты'})
            references = doctor.next_doctor.order_by('next_date').filter(next_date__date='-'.join(speks['date'].split()[0].split('-')[::-1]))


            appointments = []
            for i in references:
                appointments.append([
                    i.next_date.strftime('%H:%M'), (i.next_date + datetime.timedelta(minutes=i.lenght)).strftime('%H:%M')
                ])

            return Response({'data': appointments})

class DoctorReference(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if request.GET.get('mode') == 'new':
                return Response({"data": serializers.ReferenceSerializer(user.doctor.next_doctor.order_by('next_date')
                                .filter(next_date__gt=datetime.datetime.now() + datetime.timedelta(hours=MY_TIME_ZONE) - datetime.timedelta(minutes=30)), many=True).data})
            elif request.GET.get('mode') == 'old':
                return Response({"data": serializers.ReferenceSerializer(user.doctor.next_doctor.order_by('next_date')
                                .filter(next_date__lt=datetime.datetime.now() + datetime.timedelta(hours=MY_TIME_ZONE) - datetime.timedelta(minutes=30)), many=True).data})
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            if 'id' in speks:
                if user.doctor.is_director:
                    reference = user.doctor.hospital.reference_set.get(id=int(speks['id']))
                else:
                    try:
                        reference = user.doctor.next_doctor.get(id=int(speks['id']))
                    except:
                        return Response({"message": 'Нет такого доктора'})
                
                return Response({"data": serializers.ReferenceSerializer(reference).data})


class DoctorReferenceAllDates(APIView):
    def get(self, request):
        return Response({'messange':'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            speks = request.data
            try:
                all_dates = user.doctor.hospital.doctor_set.get(id=int(speks['id'])).next_doctor.filter(all_day=True).values_list('next_date', flat=True)
            except:
                return Response({"message": 'Нет такого пациента'})
            
            return Response({'data': all_dates})

