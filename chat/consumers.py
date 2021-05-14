# chat/consumers.py
import json
import aiml
import os
from google_trans_new import google_translator

from channels.generic.websocket import AsyncWebsocketConsumer

os.chdir("D:/Programs/Anaconda/envs/py36/Lib/site-packages/aiml/botdata/alice")
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond("load alice")
translator = google_translator()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        language = text_data_json['language']
        angMessage = translator.translate(message, lang_tgt=language)
        response = alice.respond(angMessage)
        sloMessage = translator.translate(response, lang_tgt=language)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "You: " + message+"\nSmart Alice:" + sloMessage + "\n"
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
