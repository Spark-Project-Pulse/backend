from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Badge, UserBadge, UserBadgeProgress
from ..serializers import BadgeSerializer, UserBadgeSerializer, UserBadgeProgressSerializer
from rest_framework import status

@api_view(["GET"])
def getAllBadges(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all badges from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A response containing serialized data for all badges.
    """
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserBadges(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve all badges earned by a specific user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user.

    Returns:
        JsonResponse: A response containing serialized data for the user's badges.
    """
    user_badges = UserBadge.objects.filter(user_id=user_id)
    serializer = UserBadgeSerializer(user_badges, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserBadgeProgress(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve badge progress for a specific user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user.

    Returns:
        JsonResponse: A response containing serialized data for the user's badge progress.
    """
    progress = UserBadgeProgress.objects.filter(user_id=user_id)
    serializer = UserBadgeProgressSerializer(progress, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
