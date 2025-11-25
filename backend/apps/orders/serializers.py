from rest_framework import serializers
from django.utils import timezone
from .models import Order, Offer, Message

class OrderSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    buyer_email = serializers.EmailField(source='buyer.email', read_only=True)
    offers_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'title', 'description', 'category_name', 'buyer_email',
            'budget_min', 'budget_max', 'region', 'deadline', 'status', 
            'created_at', 'is_urgent', 'offers_count'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'title', 'description', 'category', 'budget_min', 
            'budget_max', 'region', 'deadline', 'is_urgent'
        ]
    
    def validate_deadline(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Срок должен быть в будущем")
        return value
    
    def validate(self, data):
        if data.get('budget_min') and data.get('budget_max'):
            if data['budget_min'] > data['budget_max']:
                raise serializers.ValidationError(
                    "Минимальный бюджет не может быть больше максимального"
                )
        return data

class OfferSerializer(serializers.ModelSerializer):
    supplier_email = serializers.EmailField(source='supplier.email', read_only=True)
    supplier_id = serializers.IntegerField(source='supplier.id', read_only=True)
    
    class Meta:
        model = Offer
        fields = [
            'id', 'price', 'delivery_days', 'comment', 
            'supplier_email', 'supplier_id', 'created_at', 'is_selected'
        ]

class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['price', 'delivery_days', 'comment']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной")
        return value
    
    def validate_delivery_days(self, value):
        if value < 1:
            raise serializers.ValidationError("Срок поставки минимум 1 день")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender_email', 'timestamp', 'is_read']
