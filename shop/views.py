from rest_framework import viewsets, filters,generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,ContactMessage,Style, Brand, Color, Size
from .serializers import ProductSerializer,ContactMessageSerializer,BrandSerializer, ColorSerializer, SizeSerializer
from rest_framework.permissions import AllowAny
from .serializers_auth import RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related("category","brand","style").prefetch_related("colors","sizes")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "category__slug": ["exact"],
        "brand__slug": ["exact"],
        "style__name": ["exact"],
        "colors__name": ["exact"],
        "sizes__value": ["exact"],
        "is_featured": ["exact"],
    }
    search_fields = ["name","description","brand__name"]
    ordering_fields = ["price","rating","created_at"]
 # Disable DRF pagination for this view
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ContactMessageView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save()
        # Send email to admin
        send_mail(
            subject=f"New Contact Form: {contact.subject}",
            message=f"From: {contact.name} <{contact.email}>\n\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Admin email
            fail_silently=False,
        )


class FilterOptionsView(APIView):
    def get(self, request):
        # Get styles that exist in products
        styles = list(Product.objects.exclude(style__isnull=True).values_list('style__name', flat=True).distinct())
        
        # Brands that exist in products
        brands = BrandSerializer(Brand.objects.filter(products__isnull=False).distinct(), many=True).data
        colors = ColorSerializer(Color.objects.filter(products__isnull=False).distinct(), many=True).data
        sizes = SizeSerializer(Size.objects.filter(products__isnull=False).distinct(), many=True).data

        return Response({
            "styles": styles,
            "brands": [b["name"] for b in brands],
            "colors": [c["name"] for c in colors],
            "sizes": [s["value"] for s in sizes]
        })