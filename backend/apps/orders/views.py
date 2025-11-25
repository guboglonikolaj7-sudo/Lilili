from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count
from .models import Order, Offer, Message
from .serializers import (
    OrderSerializer, 
    OfferSerializer, 
    OrderCreateSerializer,
    OfferCreateSerializer,
    MessageSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(
            status='active'
        ).select_related(
            'category', 'buyer'
        ).annotate(
            offers_count=Count('offers')
        ).order_by('-is_urgent', '-created_at')

class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class OfferCreateAPIView(generics.CreateAPIView):
    serializer_class = OfferCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id, status='active')
        
        if Offer.objects.filter(order=order, supplier=request.user).exists():
            return Response(
                {"error": "Вы уже подавали предложение к этому заказу"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, supplier=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(
            buyer=self.request.user
        ).select_related('category').order_by('-created_at')

class OrderOffersAPIView(generics.ListAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id, buyer=self.request.user)
        return Offer.objects.filter(order=order).select_related('supplier')
