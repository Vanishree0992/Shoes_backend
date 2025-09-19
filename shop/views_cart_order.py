from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem, OrderStatus, Product, Size
from .serializers_cart_order import CartSerializer, CartItemSerializer, OrderSerializer, OrderStatusSerializer

# ===========================
# Cart API
# ===========================
class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return Response(CartSerializer(cart, context={"request": request}).data)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        product_id = request.data.get("product")
        size_id = request.data.get("size")
        quantity = int(request.data.get("quantity", 1))
        product = Product.objects.get(id=product_id)
        size = Size.objects.get(id=size_id) if size_id else None

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size, defaults={"quantity": quantity, "price": product.price})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item, context={"request": request}).data)


# ===========================
# Order API
# ===========================
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart or cart.items.count() == 0:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = Order.objects.create(
            user=user,
            order_number=f"ORD{user.id}{cart.id}",
            status="placed",
            payment_method=request.data.get("payment_method", "cod"),
            payment_status=False,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            email=request.data.get("email"),
            phone=request.data.get("phone"),
            address_line1=request.data.get("address_line1"),
            city=request.data.get("city"),
            state=request.data.get("state"),
            landmark=request.data.get("landmark", ""),
            pincode=request.data.get("pincode"),
            amount=cart.total_price(),
            delivery_fee=request.data.get("delivery_fee", 0)
        )

        # Copy cart items to order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.price
            )

        # Clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order, context={"request": request}).data)


# ===========================
# Order Status / Tracking
# ===========================
class OrderStatusViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        return OrderStatus.objects.filter(order__user=self.request.user)
