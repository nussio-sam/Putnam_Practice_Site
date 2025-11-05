from channels.generic.websocket import AsyncWebsocketConsumer
import json

class HintConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps({
            'message': 'Received request'
        }))
