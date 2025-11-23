from django.contrib import admin
from .models import Order, Offer, Message

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "buyer", "category", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description")

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "supplier", "price", "delivery_days", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__title", "supplier__email")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "sender", "content", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("content", "sender__email", "order__title")