from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path(
        "events/<int:event_id>/register/",
        views.register_event,
        name="register_event"
    ),
    path(
        "my-registrations/",
        views.my_registrations,
        name="my_registrations"
    ),
    path(
        "registrations/<int:registration_id>/",
        views.cancel_registration,
        name="cancel_registration"
    ),
]