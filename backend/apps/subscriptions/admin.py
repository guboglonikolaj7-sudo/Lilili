from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'contact_credits', 'duration_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'remaining_credits', 'is_active_status', 'expires_at']
    list_filter = ['plan', 'expires_at']
    search_fields = ['user__email']
    
    def is_active_status(self, obj):
        return obj.is_active()
    is_active_status.boolean = True
    is_active_status.short_description = "Активна"
