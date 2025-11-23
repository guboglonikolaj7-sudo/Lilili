from django.urls import path
from .views import SupplierListAPIView, supplier_contacts

app_name = "suppliers"

urlpatterns = [
    path("", SupplierListAPIView.as_view(), name="supplier-list"),
    path("<int:pk>/contacts/", supplier_contacts, name="supplier-contacts"),
]