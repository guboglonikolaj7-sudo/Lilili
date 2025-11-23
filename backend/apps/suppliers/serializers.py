from rest_framework import serializers
from .models import Supplier, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class SupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "country",
            "city",
            "description",
            "logo",
            "video_url",
            "moq",
            "category",
            "created_at",
        ]