from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer
from .models import Notification_user
from accounts.models import Users
from .serializers import Notification_data
from accounts.tools import get_user, decodetoken

import json

@database_sync_to_async
def gets_user(user_id):
    try:
        return Users.objects.get(id=user_id)
    except:
        return None


@database_sync_to_async
def create_notification(receiver,typeof="task_created",status="unread"):
    notification_to_create=Notification_user.objects.create(user_revoker=receiver,type_of_notification=typeof)
    print('I am here to help')
    return (notification_to_create.user_revoker.username,notification_to_create.type_of_notification)

@database_sync_to_async
def create_data(requstuser):
    notifications_unread = Notification_user.objects.filter(user=requstuser,status = "unread").count()
    notifications = Notification_user.objects.filter(user=requstuser).order_by('created_at')[:9]
    data = {
        'notifications_unread': notifications_unread + 1,
        'notifications': Notification_data(notifications, many=True).data,
    }
    return data

class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
            print('connected',event)
            print('Am i finallyy here')
            print(self.scope['user'])
            await self.accept()
            
            token = self.scope['url_route']['kwargs']['room_name']
            print(token)
            if(token == 'auth'):
                self.room_name='user_group'  
                self.room_group_name='user_group' 
                await self.channel_layer.group_add(self.room_group_name,self.channel_name)

                await self.send(json.dumps({
                    "type":"websocket.send",
                    "text":"room made"
                }))
            else:
                print("----token", token)
                requstuser=await gets_user(token)

                print("----token", token)
                print("----user", requstuser)

                self.room_name='user_group'+str(requstuser.id)  
                self.room_group_name='user_group'+str(requstuser.id) 
                await self.channel_layer.group_add(self.room_group_name,self.channel_name)
                data = await create_data(requstuser)
                await self.send(json.dumps(data))
                
    async def websocket_receive(self,event):
            print(event)
            data_to_get=json.loads(event['text'])
            """
            get_of=await create_notification(user_to_get)
            self.room_group_name='test_consumer_group'
            channel_layer=get_channel_layer()
            await (channel_layer.group_send)(
                self.room_group_name,
                {
                    "type":"send_notification",
                    "value":json.dumps(get_of)
                }
            )
            print('receive',event)
            """
            data=await sync_to_async(decodetoken)(data_to_get['token'])
            print("----data", data)
            requstuser=await sync_to_async(get_user)(*data)

            print("----token", data_to_get['token'])
            print("----user", requstuser)

            data = await create_data(requstuser)

            await self.send(json.dumps(data))
    
    async def websocket_disconnect(self,event):
            print('disconnect',event)

    async def send_notification(self,event):
            data = json.loads(event.get('value'))
            
            await self.send(json.dumps({
                "type":"websocket.send",
                "data": data
            }))
            print('Notification sent....')
            print(event)



"""
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notification'
        print("scope here", self.scope)
        await self.channel_layer.group_add(self.group_name,self.channel_name)

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        event = {
            'type': 'send_message',
            'message': message
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data = json.dumps({'message': message}))

"""  