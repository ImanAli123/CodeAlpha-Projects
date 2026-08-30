from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Event, Registration
import json


def event_list(request):
    if request.method == "GET":

        events = Event.objects.all()

        data = []

        for event in events:
            data.append({
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "date": event.date,
                "location": event.location
            })

        return JsonResponse(data, safe=False)


def event_detail(request, event_id):
    if request.method == "GET":

        try:
            event = Event.objects.get(id=event_id)

            data = {
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "date": event.date,
                "location": event.location
            }

            return JsonResponse(data)

        except Event.DoesNotExist:
            return JsonResponse(
                {"error": "Event not found"},
                status=404
            )


@csrf_exempt
def register_event(request, event_id):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            user_id = data.get("user_id")

            if not user_id:
                return JsonResponse(
                    {"error": "user_id is required"},
                    status=400
                )

            user = User.objects.get(id=user_id)
            event = Event.objects.get(id=event_id)

            existing_registration = Registration.objects.filter(
                user=user,
                event=event
            ).first()

            if existing_registration:
                return JsonResponse(
                    {"error": "User is already registered for this event"},
                    status=400
                )

            registration = Registration.objects.create(
                user=user,
                event=event
            )

            return JsonResponse({
                "message": "Registration successful",
                "registration_id": registration.id,
                "user": user.username,
                "event": event.name
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        except Event.DoesNotExist:
            return JsonResponse(
                {"error": "Event not found"},
                status=404
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )


def my_registrations(request):

    if request.method == "GET":

        user_id = request.GET.get("user_id")

        if not user_id:
            return JsonResponse(
                {"error": "user_id is required"},
                status=400
            )

        try:
            user = User.objects.get(id=user_id)

            registrations = Registration.objects.filter(
                user=user
            )

            data = []

            for registration in registrations:
                data.append({
                    "registration_id": registration.id,
                    "event_id": registration.event.id,
                    "event_name": registration.event.name,
                    "event_date": registration.event.date,
                    "event_location": registration.event.location,
                    "registration_date": registration.registration_date
                })

            return JsonResponse(data, safe=False)

        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )


@csrf_exempt
def cancel_registration(request, registration_id):

    if request.method == "DELETE":

        try:
            registration = Registration.objects.get(
                id=registration_id
            )

            registration.delete()

            return JsonResponse({
                "message": "Registration cancelled successfully"
            })

        except Registration.DoesNotExist:
            return JsonResponse(
                {"error": "Registration not found"},
                status=404
            )

    return JsonResponse(
        {"error": "Only DELETE method is allowed"},
        status=405
    )