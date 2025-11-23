from django.contrib import admin
from .models import Category, LogisticsCompany, Supplier

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(LogisticsCompany)
class LogisticsCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "site")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "category", "moq", "created_at")
    list_filter = ("country", "category", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")