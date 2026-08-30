from django.contrib import admin

from .models import (
    MenuItem,
    RestaurantTable,
    Reservation,
    Order,
    OrderItem,
    Inventory,
)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "available")
    list_filter = ("available",)
    search_fields = ("name",)


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity", "is_available")
    list_filter = ("is_available",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "customer_phone",
        "table",
        "date",
        "time",
        "guests",
    )
    list_filter = ("date",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "table",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = ("status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "menu_item",
        "quantity",
        "price",
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "menu_item",
        "quantity",
        "unit",
    )