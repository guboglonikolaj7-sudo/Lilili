from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import RFQ, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class RFQConsumer(AsyncWebsocketConsumer):
    """WebSocket для real-time сообщений по RFQ"""
    
    async def connect(self):
        self.rfq_id = self.scope['url_route']['kwargs']['rfq_id']
        self.rfq_group_name = f'rfq_{self.rfq_id}'
        
        # Присоединиться к группе
        await self.channel_layer.group_add(
            self.rfq_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Покинуть группу
        await self.channel_layer.group_discard(
            self.rfq_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Сохранить сообщение в БД
        rfq = await RFQ.objects.aget(id=self.rfq_id)
        user = self.scope['user']
        
        await Message.objects.acreate(
            rfq=rfq,
            sender=user,
            sender_type='buyer' if not hasattr(user, 'supplier_profile') else 'supplier',
            content=message
        )
        
        # Отправить сообщение всем в группе
        await self.channel_layer.group_send(
            self.rfq_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.email
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))