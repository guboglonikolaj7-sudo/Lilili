from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rfq', views.RFQViewSet, basename='rfq')
router.register(r'quotes', views.QuoteViewSet, basename='quotes')
router.register(r'messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]