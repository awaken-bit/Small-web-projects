from rest_framework import serializers
from main.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    @staticmethod
    def get_owner(obj):
        return UserSerializer(obj.owner).data

class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
    
    @staticmethod
    def get_date(obj):
        return f"{obj.date.day}-{obj.date.month}-{obj.date.year}"

    @staticmethod
    def get_time(obj):
        return f"{obj.date.hour}:{obj.date.minute}"
    
    @staticmethod
    def get_owner(obj):
        return ProfileSerializer(obj.owner).data

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
    
    @staticmethod
    def get_owner(obj):
        return ProfileSerializer(obj.owner).data