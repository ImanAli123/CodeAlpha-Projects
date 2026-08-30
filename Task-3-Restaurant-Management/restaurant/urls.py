from rest_framework.routers import DefaultRouter

from .views import (
    MenuItemViewSet,
    RestaurantTableViewSet,
    ReservationViewSet,
    OrderViewSet,
    InventoryViewSet,
)

router = DefaultRouter()

router.register("menu", MenuItemViewSet, basename="menu")
router.register("tables", RestaurantTableViewSet, basename="tables")
router.register("reservations", ReservationViewSet, basename="reservations")
router.register("orders", OrderViewSet, basename="orders")
router.register("inventory", InventoryViewSet, basename="inventory")

urlpatterns = router.urls