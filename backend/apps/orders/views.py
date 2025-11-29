from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RFQ, Quote, Message
from .serializers import RFQSerializer, QuoteSerializer, MessageSerializer

class RFQViewSet(viewsets.ModelViewSet):
    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Покупатель видит только свои RFQ
        if self.request.user.is_authenticated:
            return self.queryset.filter(buyer=self.request.user)
        return self.queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Опубликовать RFQ и уведомить поставщиков"""
        rfq = self.get_object()
        rfq.status = 'published'
        rfq.save()
        
        # Уведомить поставщиков (через WebSocket будет позже)
        return Response({'status': 'RFQ опубликован'})

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Поставщик видит только свои котировки
        if hasattr(self.request.user, 'supplier_profile'):
            return self.queryset.filter(supplier=self.request.user.supplier_profile)
        return self.queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user.supplier_profile)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(rfq__in=self.request.user.rfqs.all())