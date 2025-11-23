from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order, Offer
from .serializers import OrderSerializer, OfferSerializer, OrderCreateSerializer

# Список активных заказов
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.filter(status='active')
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

# Создание заказа
class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
   # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

# Создание предложения
class OfferCreateAPIView(generics.CreateAPIView):
    serializer_class = OfferSerializer
    # permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs['order_id'], status='active')
        if Offer.objects.filter(order=order, supplier=self.request.user).exists():
            raise serializers.ValidationError("Вы уже подавали предложение к этому заказу")
        serializer.save(order=order, supplier=self.request.user)