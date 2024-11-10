from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Notifications
from rest_framework import status
from ..serializers import NotificationSerializer


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
