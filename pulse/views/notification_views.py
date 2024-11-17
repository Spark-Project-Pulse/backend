from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Notifications
from rest_framework import status
from ..serializers import NotificationSerializer
from uuid import UUID
from services.notification_service import NotificationService


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
def getNotificationsCountByUserId(request: HttpRequest, user_id: int) -> JsonResponse:
    """
    Retrieve number of notifications for a user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The ID of the user whose Notifications are to be retrieved.

    Returns:
        JsonResponse: A response containing the number of Notifications for a user.
    """
    count = Notifications.objects.filter(recipient_id=user_id).count()
    return JsonResponse({"count": count}, safe=False, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def markAsRead(request: HttpRequest, user_id: str, notification_id: str) -> JsonResponse:
    """
    Retrieve all notifications from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: Success/failure message with appropriate status code
    """

    try:
        user_id = UUID(user_id) # TODO: we should really add middleware at some point and use a JWT to get access to the current user in the BACKEND
        notification_id = UUID(notification_id)
    except (ValueError, TypeError):
        return JsonResponse(
            {"error": "Invalid notification/user ID format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    success = NotificationService.mark_as_read(user_id, notification_id)
    
    if success:
        return JsonResponse(
            {"message": "Notification marked as read"}, 
            status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            {"error": "Notification not found or unauthorized"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PATCH"])
def markAsUnread(request: HttpRequest, user_id: str, notification_id: str) -> JsonResponse:
    """
    Retrieve all notifications from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: Success/failure message with appropriate status code
    """

    try:
        user_id = UUID(user_id) # TODO: we should really add middleware at some point and use a JWT to get access to the current user in the BACKEND
        notification_id = UUID(notification_id)
    except (ValueError, TypeError):
        return JsonResponse(
            {"error": "Invalid notification/user ID format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    success = NotificationService.mark_as_unread(user_id, notification_id)
    
    if success:
        return JsonResponse(
            {"message": "Notification marked as unread"}, 
            status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            {"error": "Notification not found or unauthorized"}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def deleteNotification(request: HttpRequest, user_id: str, notification_id: str) -> JsonResponse:
    """
    Delete a notification if the authenticated user is the recipient.

    Args:
        request (HttpRequest): The incoming HTTP request
        notification_id (str): UUID of the notification to delete

    Returns:
        JsonResponse: Success/failure message with appropriate status code
    """
    try:
        user_id = UUID(user_id) # TODO: we should really add middleware at some point and use a JWT to get access to the current user in the BACKEND
        notification_id = UUID(notification_id)
    except ValueError:
        return JsonResponse(
            {"error": "Invalid notification ID format"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    success = NotificationService.delete(user_id, notification_id)
    
    if success:
        return JsonResponse(
            {"message": "Notification deleted successfully"}, 
            status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            {"error": "Notification not found or unauthorized"}, 
            status=status.HTTP_404_NOT_FOUND
        )