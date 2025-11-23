from django.urls import path
from .views import OrderListAPIView, OrderCreateAPIView, OfferCreateAPIView

app_name = "orders"

urlpatterns = [
    path("", OrderListAPIView.as_view(), name="order-list"), 
    path("orders/", OrderListAPIView.as_view(), name="order-list"),
    path("orders/create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("orders/<int:order_id>/offers/", OfferCreateAPIView.as_view(), name="offer-create"),
]