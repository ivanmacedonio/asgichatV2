import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Box

class BoxConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] #extraemos el room name de la url
        self.room_group_name = "chat%s" % self.room_name #y lo almacenamos en una variable

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        #el cliente envia info y el server la recibe 
    async def receive(self,data):
            data_json = json.loads(data)
            box_id = data_json["box_id"]
            title = data_json["title"]
            color = data_json["color"]

            #enviamos el mensaje a la sala
            await self.channel_layer.group_send(
                self.room_group_name,{
                "type": "box",
                "title": title,
                "color": color,
                "id" : box_id,
            },
            )

            try:
                box = Box.objects.get(pk=box_id)
                box.title = data.get('title')
                box.color = data.get('color')
                box.save()
                
            except Box.DoesNotExist:
                pass

            

    async def box_dump(self,event):
            #recibimos informacion de la sala
            box_id = event["box_id"]
            title = event["title"]
            color = event["color"]

            
            await self.send(
                text_data = json.dumps({
                    "type": "box",
                    "id": box_id,
                    "title": title,
                    "color": color,
                },
                )
            )

