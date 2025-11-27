from rest_framework import serializers
from .models import Supplier, Category, LogisticsCompany, VerificationCheck

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

class VerificationCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCheck
        fields = [
            "id",
            "supplier",
            "country",
            "status",
            "fssp_score",
            "rnp_score",
            "egrul_score",
            "licenses_score",
            "overall_score",
            "risk_level",
            "is_verified",
            "checked_sources",
            "error_message",
            "started_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]


class SupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    logistics_options = LogisticsSerializer(read_only=True, many=True)
    logo_url = serializers.SerializerMethodField()
    latest_check = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "country",
            "city",
            "description",
            "logo",
            "logo_url",
            "video_url",
            "moq",
            "contact_email",
            "contact_phone",
            "category",
            "logistics_options",
            "verification_status",
            "verification_score",
            "is_verified",
            "last_verified_at",
            "latest_check",
            "created_at",
        ]

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

    def get_latest_check(self, obj):
        check = obj.verification_checks.order_by("-created_at").first()
        if not check:
            return None
        return VerificationCheckSerializer(check).data
