import requests
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'voicebot_%s' % self.room_name

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
        id = text_data_json['id']
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'id': id,
            'message': message
        }))
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': id,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        id = event['id']
        message = event['message']

        input = {'message': message}
        try:
            response = requests.post('http://127.0.0.9:8080/predict/', data=input)
            result = response.json()
        except:
            result = {'message': '서버와 연결할 수 없습니다'}

        id = 1
        message = result['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': id,
            'message': message
        }))