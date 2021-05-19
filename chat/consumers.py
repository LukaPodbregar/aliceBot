# chat/consumers.py
import json
import aiml
import os
from google_trans_new import google_translator

from channels.generic.websocket import AsyncWebsocketConsumer

#Change the path to your aiml library
os.chdir("../Lib/site-packages/aiml/botdata/alice")
#Initiating aiml Kernel
alice = aiml.Kernel()
#Initiating Alice with startup.xml
alice.learn("startup.xml")
#Setting Alice's name
alice.setPredicate("Alice", "name")
#Learning aiml knowledge
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
        #Saving language that is selected in the UI
        language = text_data_json['language']
        #Checking if language is english or not english, the latter needs to be translated first and then translated back
        if language is 'en':
            response = alice.respond(message)
        else:
            #Message is translated to english
            angMessage = translator.translate(message, lang_tgt='en')
            #Create Alice's response to the message
            responseAlice = alice.respond(angMessage)
            #Translate the response to the proper language
            response = translator.translate(responseAlice, lang_tgt=language)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "You: " + message+"\nSmart Alice: " + response + "\n"
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
