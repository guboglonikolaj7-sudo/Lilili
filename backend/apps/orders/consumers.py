import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Order


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.order_id}'
        
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        # Проверяем существование заказа
        order_exists = await self.check_order_exists()
        if not order_exists:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Отправляем историю сообщений
        await self.send_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        saved_message = await self.save_message(message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].email,
                'timestamp': saved_message['timestamp']
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def check_order_exists(self):
        return Order.objects.filter(id=self.order_id).exists()

    @database_sync_to_async
    def get_message_history(self):
        messages = Message.objects.filter(order_id=self.order_id).order_by('timestamp')[:50]
        return [
            {
                'id': msg.id,
                'content': msg.content,
                'sender': msg.sender.email,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]

    async def send_history(self):
        history = await self.get_message_history()
        for msg in history:
            await self.send(text_data=json.dumps({
                'message': msg['content'],
                'sender': msg['sender'],
                'timestamp': msg['timestamp']
            }))

    @database_sync_to_async
    def save_message(self, content):
        from django.utils import timezone
        order = Order.objects.get(id=self.order_id)
        msg = Message.objects.create(
            order=order,
            sender=self.scope['user'],
            content=content
        )
        return {
            'id': msg.id,
            'timestamp': msg.timestamp.isoformat()
        }
