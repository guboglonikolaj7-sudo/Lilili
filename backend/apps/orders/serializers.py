from rest_framework import serializers
from .models import RFQ, Quote, Message

class RFQSerializer(serializers.ModelSerializer):
    buyer_email = serializers.CharField(source='buyer.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    quotes_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = RFQ
        fields = '__all__'
        read_only_fields = ['buyer']

class QuoteSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'
        read_only_fields = ['supplier']

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'