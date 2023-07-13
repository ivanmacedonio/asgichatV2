import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] #extraemos el room name de la url
        self.room_group_name = "chat%s" % self.room_name #y lo almacenamos en una variable

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        #el cliente envia info y el server la recibe 
    async def receive(self,text_data):
            text_data_json = json.loads(text_data)
            name = text_data_json["name"]
            text = text_data_json["text"]

            #enviamos el mensaje a la sala
            await self.channel_layer.group_send(
                self.room_group_name,{
                "type": "chat_message",
                "name": name,
                "text": text,
            },
            )

    async def chat_message(self,event):
            #recibimos informacion de la sala
            name = event["name"]
            text = event["text"]

            #enviamos mensaje al websocket(enviamos el mensaje al cliente, lo recibe)
            await self.send(
                text_data = json.dumps({
                    "type": "chat_message",
                    "name": name,
                    "text": text,
                },
                )
            )

