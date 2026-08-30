from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import (
    MenuItem,
    RestaurantTable,
    Reservation,
    Order,
    OrderItem,
    Inventory,
)

from .serializers import (
    MenuItemSerializer,
    RestaurantTableSerializer,
    ReservationSerializer,
    OrderSerializer,
    InventorySerializer,
)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class RestaurantTableViewSet(viewsets.ModelViewSet):
    queryset = RestaurantTable.objects.all()
    serializer_class = RestaurantTableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.select_related("menu_item").all()
    serializer_class = InventorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        customer_name = request.data.get("customer_name")
        table_id = request.data.get("table")
        items = request.data.get("items", [])

        if not customer_name:
            return Response(
                {"error": "Customer name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not items:
            return Response(
                {"error": "At least one order item is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        table = None

        if table_id:
            try:
                table = RestaurantTable.objects.get(id=table_id)
            except RestaurantTable.DoesNotExist:
                return Response(
                    {"error": "Table not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        total_price = 0
        order_items_data = []

        for item in items:
            try:
                menu_item = MenuItem.objects.get(
                    id=item["menu_item"],
                    available=True
                )
            except (MenuItem.DoesNotExist, KeyError):
                return Response(
                    {"error": "Invalid or unavailable menu item."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                quantity = int(item["quantity"])
            except (ValueError, TypeError, KeyError):
                return Response(
                    {"error": "Quantity must be a valid number."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if quantity <= 0:
                return Response(
                    {"error": "Quantity must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                inventory = Inventory.objects.select_for_update().get(
                    menu_item=menu_item
                )
            except Inventory.DoesNotExist:
                return Response(
                    {
                        "error": f"No inventory record found for {menu_item.name}."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if inventory.quantity < quantity:
                return Response(
                    {
                        "error": (
                            f"Insufficient stock for {menu_item.name}. "
                            f"Available: {inventory.quantity}"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item_price = menu_item.price
            total_price += item_price * quantity

            order_items_data.append(
                {
                    "menu_item": menu_item,
                    "quantity": quantity,
                    "price": item_price,
                    "inventory": inventory,
                }
            )

        order = Order.objects.create(
            customer_name=customer_name,
            table=table,
            total_price=total_price,
        )

        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                menu_item=item_data["menu_item"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

            inventory = item_data["inventory"]
            inventory.quantity -= item_data["quantity"]
            inventory.save()

        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )