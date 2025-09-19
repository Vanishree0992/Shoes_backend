from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, OrderStatus, Product, Size

# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_name", "product_image", "size", "quantity", "price", "subtotal")

    subtotal = serializers.SerializerMethodField()

    def get_subtotal(self, obj):
        return obj.subtotal()

    def get_product_image(self, obj):
        request = self.context.get("request")
        if obj.product.image:
            return request.build_absolute_uri(obj.product.image.url)
        return None

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "created_at", "items", "total")

    def get_total(self, obj):
        return obj.total_price()


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "size", "quantity", "price", "subtotal")

    subtotal = serializers.SerializerMethodField()
    def get_subtotal(self, obj):
        return obj.subtotal()


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
        return obj.total()


# OrderStatus Serializer
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ("id", "status", "note", "location", "created_at")
