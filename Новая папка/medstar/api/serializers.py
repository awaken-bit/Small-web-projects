from rest_framework import serializers
from main.models import *
from main.views import blood_type_format


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

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

class PatientSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()
    diseases = serializers.SerializerMethodField()
    blood_type_format = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
    
    @staticmethod
    def get_birth_date(obj):
        return obj.birth_date.strftime("%d-%m-%Y")
    
    @staticmethod
    def get_diseases(obj):
        return [i.name for i in obj.diseases.all()]

    @staticmethod
    def get_blood_type_format(obj):
        return blood_type_format(obj.blood_type)