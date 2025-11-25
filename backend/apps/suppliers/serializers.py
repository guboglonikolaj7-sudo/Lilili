from rest_framework import serializers
from .models import Supplier, Category, LogisticsCompany

class CategorySerializer(serializers.ModelSerializer):
    supplier_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "supplier_count"]
    
    def get_supplier_count(self, obj):
        return obj.suppliers.filter(is_active=True).count()

class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsCompany
        fields = ["id", "name", "site", "description"]

class SupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    logistics_options = LogisticsSerializer(read_only=True, many=True)
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            "id", "name", "country", "city", "description", "logo", "logo_url",
            "video_url", "moq", "contact_email", "contact_phone", "category",
            "logistics_options", "created_at",
        ]
    
    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
