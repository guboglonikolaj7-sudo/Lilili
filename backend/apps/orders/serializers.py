from rest_framework import serializers
from django.utils import timezone
from .models import Order, Offer

class OrderSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    buyer_email = serializers.EmailField(source='buyer.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'title', 'description', 'category_name', 'buyer_email',
            'budget_min', 'budget_max', 'region', 'deadline', 'status', 'created_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['title', 'description', 'category', 'budget_min', 'budget_max', 'region', 'deadline']
    
    def validate_deadline(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Срок подачи предложений должен быть в будущем")
        return value
    
    def validate(self, data):
        if data.get('budget_min') and data.get('budget_max'):
            if data['budget_min'] > data['budget_max']:
                raise serializers.ValidationError("Минимальный бюджет не может быть больше максимального")
        return data


class OfferSerializer(serializers.ModelSerializer):
    supplier_email = serializers.EmailField(source='supplier.email', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'price', 'delivery_days', 'comment', 'supplier_email', 'created_at']