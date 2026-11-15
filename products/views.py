from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from users.permissions import IsSeller, IsMarketplaceAdmin
from rest_framework.parsers import MultiPartParser, FormParser

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsMarketplaceAdmin()]
        return [AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsMarketplaceAdmin()]
        return [AllowAny()]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related("images")

        if self.request.query_params.get("mine") and self.request.user.is_authenticated:
            queryset = queryset.filter(seller=self.request.user)

        name = self.request.query_params.get("name")
        category = self.request.query_params.get("category")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category_id=category)

        ordering = self.request.query_params.get("ordering")
        if ordering == "price":
            queryset = queryset.order_by("price")
        elif ordering == "-price":
            queryset = queryset.order_by("-price")

        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def get_queryset(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return Product.objects.filter(seller=self.request.user).prefetch_related("images")
        return Product.objects.all().prefetch_related("images")


class ProductImageCreateView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            pk=self.kwargs["product_id"],
            seller=self.request.user
        )
        serializer.save(product=product)

class ProductImageDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        return ProductImage.objects.filter(
            product_id=self.kwargs["product_id"],
            product__seller=self.request.user,
        )

