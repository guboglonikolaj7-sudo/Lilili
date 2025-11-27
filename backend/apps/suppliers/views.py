from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Supplier, Category, LogisticsCompany
from .serializers import (
    SupplierSerializer,
    CategorySerializer,
    LogisticsSerializer,
    VerificationCheckSerializer,
)
from rest_framework.pagination import PageNumberPagination
from .tasks import verify_supplier_task, batch_verify_suppliers


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Supplier.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("logistics_options", "verification_checks")
    )
    serializer_class = SupplierSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country", "category__slug", "city", "moq"]
    search_fields = ["name", "description", "country", "city"]
    ordering_fields = ["created_at", "moq", "name"]
    ordering = ["-created_at"]

    @action(detail=True, methods=["get"])
    def contacts(self, request, pk=None):
        supplier = self.get_object()
        return Response(
            {
                "contact_email": supplier.contact_email,
                "contact_phone": supplier.contact_phone,
                "name": supplier.name,
            }
        )

    @action(detail=True, methods=["get"])
    def verification_checks(self, request, pk=None):
        supplier = self.get_object()
        serializer = VerificationCheckSerializer(
            supplier.verification_checks.all(), many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        supplier = self.get_object()
        task = verify_supplier_task.delay(supplier.id)
        return Response(
            {
                "task_id": task.id,
                "message": "Проверка запущена. Результат появится автоматически.",
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["post"])
    def verify_all(self, request):
        supplier_ids = request.data.get("supplier_ids")
        if supplier_ids and not isinstance(supplier_ids, list):
            return Response(
                {"detail": "supplier_ids должен быть массивом ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        batch_verify_suppliers.delay(supplier_ids)
        return Response(
            {"message": "Пакетная проверка поставщиков запущена."},
            status=status.HTTP_202_ACCEPTED,
        )


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class LogisticsListAPIView(generics.ListAPIView):
    queryset = LogisticsCompany.objects.all()
    serializer_class = LogisticsSerializer
    permission_classes = [AllowAny]
