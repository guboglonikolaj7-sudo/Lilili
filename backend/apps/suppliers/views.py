from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["country", "category__slug"]
    search_fields = ["name", "description"]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def supplier_contacts(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return Response({
        "contact_email": supplier.contact_email,
        "contact_phone": supplier.contact_phone,
    })