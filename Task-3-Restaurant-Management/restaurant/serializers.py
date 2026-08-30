from rest_framework import serializers
from .models import (
    MenuItem,
    RestaurantTable,
    Reservation,
    Order,
    OrderItem,
    Inventory,
)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, data):
        table = data["table"]
        date = data["date"]
        time = data["time"]

        existing_reservation = Reservation.objects.filter(
            table=table,
            date=date,
            time=time
        ).exists()

        if existing_reservation:
            raise serializers.ValidationError(
                "This table is already reserved for this date and time."
            )

        if data["guests"] > table.capacity:
            raise serializers.ValidationError(
                "Number of guests exceeds table capacity."
            )

        return data


class InventorySerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(
        source="menu_item.name",
        read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "menu_item",
            "menu_item_name",
            "quantity",
            "unit",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(
        source="menu_item.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "menu_item",
            "menu_item_name",
            "quantity",
            "price",
        ]
        read_only_fields = ["price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "table",
            "status",
            "total_price",
            "created_at",
            "items",
        ]
        read_only_fields = [
            "total_price",
            "created_at",
            "status",
        ]