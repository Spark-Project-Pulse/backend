from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Notifications
from rest_framework import status
from ..serializers import NotificationSerializer


@api_view(["GET"])
def getNotificationsByUserId(request: HttpRequest, user_id: int) -> JsonResponse:
    """
    Retrieve all Notifications associated with a specific user_id
    from the database and serialize them to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The ID of the user whose Notifications are to be retrieved.

    Returns:
        JsonResponse: A response containing serialized data for the user's Notifications.
    """
    notifications = Notifications.objects.filter(recipient_id=user_id).order_by(
        "-created_at"
    )  # Retrieve Notifications for the specified user
    serializer = NotificationSerializer(
        notifications, many=True
    )  # Serialize the queryset to JSON
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getAllNotifications(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all notifications from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        Json
    """
    tags = Notifications.objects.all()
    serializer = NotificationSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
