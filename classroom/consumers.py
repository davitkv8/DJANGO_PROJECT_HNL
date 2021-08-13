from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Message
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name =self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat' + self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_py = json.loads(text_data)

        message = text_data_py['message']
        sender = text_data_py['sender']
        receiver = text_data_py['receiver']
        await database_sync_to_async(self.send_message_to_DB)(message, sender, receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
            }
        )

    def send_message_to_DB(self, message=None, sender=None, receiver=None):
        return Message.objects.create(message=message,
                                      sender=User.objects.get(username=sender),
                                      receiver=User.objects.get(username=receiver))

    async def chatroom_message(self, event):
        message = event['message']
        username = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))





