from django.contrib import admin
from .models import Category, Brand, Style, Color, Size, Product,Cart, CartItem, Order, OrderItem, OrderStatus


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex")

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("value",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "price", "stock", "is_featured", "created_at")
    list_filter = ("category", "brand", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "size", "quantity", "price")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "payment_method", "amount", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("order_number", "user__username", "email", "phone")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "size", "quantity", "price")

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "location", "created_at")
    list_filter = ("status",)