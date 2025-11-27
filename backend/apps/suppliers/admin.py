from django.contrib import admin
from .models import Category, LogisticsCompany, Supplier, VerificationCheck

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(LogisticsCompany)
class LogisticsCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "site")

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "category",
        "moq",
        "verification_status",
        "verification_score",
        "is_verified",
        "created_at",
    )
    list_filter = ("country", "category", "verification_status", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("verification_status", "verification_score", "last_verified_at")


@admin.register(VerificationCheck)
class VerificationCheckAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "status",
        "overall_score",
        "risk_level",
        "is_verified",
        "completed_at",
    )
    list_filter = ("status", "risk_level", "country", "completed_at")
    search_fields = ("supplier__name",)
    autocomplete_fields = ("supplier",)