
from rest_framework import serializers

from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
        ]
        read_only_fields = ["id", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, allow_empty=False)


    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "created_at",
            "items",
        ]
        read_only_fields = [
            "id",
            "customer",
            "status",
            "created_at",
        ]

    def validate_items(self, items_data):
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Недостаточно товара {product.name} на складе. "
                    f"Доступно: {product.stock}."
                )

        return items_data

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            product.stock -= quantity
            product.save()

        return order
