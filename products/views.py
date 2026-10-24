
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from users.permissions import IsSeller, IsMarketplaceAdmin


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
        queryset = Product.objects.all()

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
            return Product.objects.filter(seller=self.request.user)

        return Product.objects.all()
