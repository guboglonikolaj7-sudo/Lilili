from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SupplierViewSet, CategoryListAPIView, LogisticsListAPIView

app_name = "suppliers"

router = DefaultRouter()
router.register("", SupplierViewSet, basename="supplier")

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("logistics/", LogisticsListAPIView.as_view(), name="logistics-list"),
    path("", include(router.urls)),
]