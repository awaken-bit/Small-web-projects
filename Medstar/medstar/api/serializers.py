from rest_framework import serializers
from main.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = '__all__'
    
    @staticmethod
    def get_user(obj):
        return UserSerializer(obj.user).data
    
    @staticmethod
    def get_department(obj):
        if obj.department:
            return obj.department.title
        else:
            return None

class DoctorSerializerForDoctors(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        exclude = ('password',)
    
    @staticmethod
    def get_user(obj):
        return UserSerializer(obj.user).data
    
    @staticmethod
    def get_department(obj):
        if obj.department:
            return obj.department.title
        else:
            return None

class PatientSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()
    diseases = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
    
    @staticmethod
    def get_birth_date(obj):
        return obj.birth_date.strftime("%d-%m-%Y")
    
    @staticmethod
    def get_diseases(obj):
        return [i.name for i in obj.diseases.all()]

class ReferenceSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    next_doctor = serializers.SerializerMethodField()
    today_date = serializers.SerializerMethodField()
    next_date =serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = '__all__'
    
    @staticmethod
    def get_patient(obj):
        return PatientSerializer(obj.patient).data
    
    @staticmethod
    def get_doctor(obj):
        return DoctorSerializerForDoctors(obj.doctor).data
    
    @staticmethod
    def get_next_doctor(obj):
        return DoctorSerializerForDoctors(obj.next_doctor).data
    
    @staticmethod
    def get_next_date(obj):
        return obj.next_date.strftime("%d-%m-%Y %H:%M")
    
    @staticmethod
    def get_today_date(obj):
        return obj.today_date.strftime("%d-%m-%Y %H:%M")