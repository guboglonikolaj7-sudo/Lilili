from django.contrib import admin
from .models import RFQ, Quote, Message

@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ('title', 'buyer', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('rfq', 'supplier', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('rfq', 'sender', 'sender_type', 'timestamp')
    list_filter = ('sender_type', 'timestamp')