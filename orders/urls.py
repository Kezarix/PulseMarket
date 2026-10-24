from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCancelView,
    OrderConfirmView,
    SellerOrderListView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("seller/", SellerOrderListView.as_view(), name="seller-order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
    path("<int:pk>/confirm/", OrderConfirmView.as_view(), name="order-confirm"),
]
