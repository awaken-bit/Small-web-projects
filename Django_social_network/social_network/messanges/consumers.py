import json

from django.contrib.contenttypes.models import ContentType

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from main.models import *
import datetime


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.addressee_id = self.scope['url_route']['kwargs']['addressee_id']
        self.list_id = [self.sender_id, self.addressee_id]
        
        self.chat_group_name = f'chat_{max(self.list_id)}_{min(self.list_id)}'
        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']
        new_comment = await self.create_new_comment(comment)
        
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'new_comment',
                'message': new_comment
            }
        )

    # Receive message from room group
    async def new_comment(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_comment(self, text):
        sender_user = Profile.objects.get(owner=self.scope['user'])
        addresseen = 0
        if int(self.list_id[0]) == self.scope['user'].id:
            addresseen = int(self.list_id[1])
        else:
            addresseen = int(self.list_id[0])

        addressee_user = Profile.objects.get(owner__id=addresseen)
        new_comment = Messange(
            sender=sender_user,
            addressee=addressee_user,
            text=text,
            pub_date=datetime.datetime.today()
        )
        new_comment.save()
        if new_comment.sender.image:
            data = {
                'date':f"{new_comment.pub_date.day}-{new_comment.pub_date.month}-{new_comment.pub_date.year}    \
                    {new_comment.pub_date.hour}:{new_comment.pub_date.minute}",
                'sender_image':new_comment.sender.image.url,
                'sender_id': new_comment.sender.owner.id,
                'first_name': new_comment.sender.owner.first_name,
                'last_name': new_comment.sender.owner.last_name,
                'text': text
            }
        else:
            data = {
                'date':f"{new_comment.pub_date.day}-{new_comment.pub_date.month}-{new_comment.pub_date.year}    \
                    {new_comment.pub_date.hour}:{new_comment.pub_date.minute}",
                'sender_id': new_comment.sender.owner.id,
                'first_name': new_comment.sender.owner.first_name,
                'last_name': new_comment.sender.owner.last_name,
                'text': text
            }
        print(data['date'])
        return data


class ChatGroupConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']

        
        self.chat_group_name = f'group_{self.group_id}'
        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['text']
        new_comment = await self.create_new_comment(comment)
        
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'new_comment',
                'message': new_comment
            }
        )

    # Receive message from room group
    async def new_comment(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_new_comment(self, text):
        sender_user = Profile.objects.get(owner=self.scope['user'])
        group_adress = Group.objects.get(id=self.group_id)
        new_comment = MessangeGroup(
            sender=sender_user,
            addressee_group=group_adress,
            text=text,
            pub_date=datetime.datetime.today()
        )
        new_comment.save()
        if new_comment.sender.image:
            data = {
                'date':f"{new_comment.pub_date.day}-{new_comment.pub_date.month}-{new_comment.pub_date.year}    \
                    {new_comment.pub_date.hour}:{new_comment.pub_date.minute}",
                'sender_image':new_comment.sender.image.url,
                'sender_id': new_comment.sender.owner.id,
                'first_name': new_comment.sender.owner.first_name,
                'last_name': new_comment.sender.owner.last_name,
                'text': text
            }
        else:
            data = {
                'date':f"{new_comment.pub_date.day}-{new_comment.pub_date.month}-{new_comment.pub_date.year}    \
                    {new_comment.pub_date.hour}:{new_comment.pub_date.minute}",
                'sender_id': new_comment.sender.owner.id,
                'first_name': new_comment.sender.owner.first_name,
                'last_name': new_comment.sender.owner.last_name,
                'text': text
            }
        return data