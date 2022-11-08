from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwarg']['nome_sala']
        self.room_group_name = f'chat_{self.room_name}'

        #entrar na sala
        await self.channel_layer.group_ad(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        #sai da sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #Recebe mensagem do WebSoquet
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensagem = text_data_json['mensagem']

        #envia a memsagem para a sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': mensagem
            }
        )

    #Recebe a mensagem do WebSocket
    async def chat_message(self, event):
        mensagem = event['message']

        #Envia MEnsagem para a sala
        await self.send(text_data=json.dumps({
            'mensagem': mensagem
        }))