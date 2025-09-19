from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilterOptionsView, ProductViewSet,RegisterView,ContactMessageView
from .views_cart_order import CartViewSet, CartItemViewSet, OrderViewSet, OrderStatusViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cart-item")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-status", OrderStatusViewSet, basename="order-status")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("contact/", ContactMessageView.as_view(), name="contact"),
    path("filters/", FilterOptionsView.as_view(), name="filter-options")
]
