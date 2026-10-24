from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(
                pk=pk,
                customer=request.user,
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.status != Order.Status.AWAITING:
            return Response(
                {"detail": "Можно отменить только ожидающий заказ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status"])

        return Response(OrderSerializer(order).data)


class OrderConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != "SELLER":
            return Response(
                {"detail": "Подтвердить заказ может только продавец."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.get(
                pk=pk,
                items__product__seller=request.user,
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ не найден или не содержит ваших товаров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.status != Order.Status.AWAITING:
            return Response(
                {"detail": "Можно подтвердить только ожидающий заказ."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = Order.Status.CONFIRMED
        order.save(update_fields=["status"])

        return Response(OrderSerializer(order).data)


class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "SELLER":
            return Order.objects.none()

        return Order.objects.filter(
            items__product__seller=self.request.user
        ).distinct()
