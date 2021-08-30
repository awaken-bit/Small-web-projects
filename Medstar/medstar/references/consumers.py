import json
from asgiref.sync import sync_to_async
from django.contrib.contenttypes.models import ContentType
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from main.models import *
from main import forms
import datetime
from medstar.settings import MY_TIME_ZONE

class ReferenceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.next_doctor_id = int(self.scope['url_route']['kwargs']['next_doctor_id'])
            self.next_doctor_obj = await self.next_doctor()
            if self.next_doctor_obj == None:
                await self.close()
            
            self.group_name = f'doctor_{self.next_doctor_id}'
            # Join room group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

        else:
            await self.close()

        await self.accept()
            
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        form = forms.ReferenceCreateForm(data_json)
        
        
        new_reference = await self.create_new_reference(form)
        if new_reference:
            # Send message to room group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': "new_comment",
                    'message': new_reference
                }
            )
            print('Проверка прошла', new_reference)
            print(self.user.doctor, self.next_doctor_obj)

    # Receive message from room group
    async def new_comment(self, event):
        if self.next_doctor_obj:
            message = event['message']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message
            }))

    @database_sync_to_async
    def create_new_reference(self, form):
        if form.is_valid() and form.cleaned_data['patient'].hospital == self.user.doctor.hospital \
                and form.cleaned_data['next_doctor'].hospital == self.user.doctor.hospital:
            reference = form.save(commit=False)

            reference.hospital = self.user.doctor.hospital
            reference.department = self.user.doctor.department
            
            try:
                if int(form.data['lenght']) > 0:
                    reference.lenght = int(form.data['lenght'])
            except:
                pass
            reference.today_date = datetime.datetime.now() + datetime.timedelta(hours=MY_TIME_ZONE)
            reference.doctor = self.user.doctor
            reference.save()
            return True
        else:
            return False

    @database_sync_to_async
    def next_doctor(self):
        try:
            next_doctor = Doctor.objects.get(id=self.next_doctor_id, hospital=self.user.doctor.hospital)
        except:
            return None
        return next_doctor == self.user.doctor
