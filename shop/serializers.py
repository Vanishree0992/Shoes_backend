from rest_framework import serializers
from .models import ContactMessage, Product, Category, Brand, Color, Size

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id","name","slug")

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id","name","slug")

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id","name","hex")

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id","value")

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField() 
    brand = BrandSerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id","name","slug","description","price","mrp","image_url","stock",
                  "category","brand","style","colors","sizes","rating","is_featured","created_at")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ("id", "name", "email", "subject", "message", "created_at")