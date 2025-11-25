from django.urls import path
from .views import (
    OrderListAPIView, OrderCreateAPIView, OfferCreateAPIView,
    MyOrdersAPIView, OrderOffersAPIView
)

app_name = "orders"

urlpatterns = [
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("my/", MyOrdersAPIView.as_view(), name="my-orders"),
    path("my/<int:order_id>/offers/", OrderOffersAPIView.as_view(), name="order-offers"),
    path("<int:order_id>/offers/", OfferCreateAPIView.as_view(), name="offer-create"),
]
