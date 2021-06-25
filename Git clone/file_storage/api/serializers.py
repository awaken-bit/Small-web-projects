from main.views import timedelta_to_dhms
from rest_framework import serializers
from main.models import *
import datetime

class RepositorySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    
    class Meta:
        model = Repository
        fields = ['id', 'name', 'time', 'username']

    @staticmethod
    def get_username(obj):
        return obj.owner.slug
    
    @staticmethod
    def get_time(obj):
        return timedelta_to_dhms(
            datetime.datetime.today() - datetime.datetime(
                    obj.changed_at.year, 
                    obj.changed_at.month, 
                    obj.changed_at.day,
                    obj.changed_at.hour,
                    obj.changed_at.minute
            )
        )