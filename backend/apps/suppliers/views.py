from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Supplier, Category, LogisticsCompany
from .serializers import SupplierSerializer, CategorySerializer, LogisticsSerializer
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.select_related('category').prefetch_related(
        'logistics_options'
    ).filter(is_active=True)
    serializer_class = SupplierSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country", "category__slug", "city", "moq"]
    search_fields = ["name", "description", "country", "city"]
    ordering_fields = ["created_at", "moq", "name"]
    ordering = ["-created_at"]

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class LogisticsListAPIView(generics.ListAPIView):
    queryset = LogisticsCompany.objects.all()
    serializer_class = LogisticsSerializer
    permission_classes = [AllowAny]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def supplier_contacts(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, is_active=True)
    return Response({
        "contact_email": supplier.contact_email,
        "contact_phone": supplier.contact_phone,
        "name": supplier.name,
    })
