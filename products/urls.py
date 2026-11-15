from django.urls import path

from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductImageCreateView,
    ProductImageDeleteView,
)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("", ProductListCreateView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:product_id>/images/", ProductImageCreateView.as_view(), name="product-image-add"),
    path("<int:product_id>/images/<int:image_id>/", ProductImageDeleteView.as_view(), name="product-image-delete"),
]