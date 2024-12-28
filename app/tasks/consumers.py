# tasks/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        
        await self.accept()
        
        self.user_id = self.scope['user'].id  
        self.group_name = f"user_{self.user_id}"  

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def task_notification(self, event):
        """
        Receive notification of new task.
        """
        await self.send_json({
            "message": event["message"],
            "task_id": event["task_id"],
        })

        