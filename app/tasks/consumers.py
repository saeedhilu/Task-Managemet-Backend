# tasks/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("...user......")
        print(self.scope.get("user"))

        await self.accept()
        
        self.user_id = self.scope['user'].id  # Get the logged-in user ID
        print('User ID: {}'.format(self.user_id))
        self.group_name = f"user_{self.user_id}"  # Group name for the user
        print(self.group_name)
        
        # Join the group associated with the user
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        
        # Accept the WebSocket connection
        

    async def disconnect(self, close_code):
        print("Disconnecting from")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def task_notification(self, event):
        print("inside task_notification")

        await self.send_json({
            "message": event["message"],
            "task_id": event["task_id"],
        })

        