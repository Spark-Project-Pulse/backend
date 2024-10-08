from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from ..models import Users
from ..serializers import UserSerializer


@api_view(["POST"])
def createUser(request: HttpRequest) -> JsonResponse:
    """
    Create a user using the UserSerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.
    
    Returns:
        JsonResponse: A response with the created user's ID if successful,
        or validation errors if the data is invalid.
    """
    serializer = UserSerializer(data=request.data)  # Deserialize and validate the data
    if serializer.is_valid():
        user = serializer.save()  # Save the valid data as a new User instance
        return JsonResponse(
            {"user_id": user.user_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getUserById(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve a single user by their ID and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested user.
    """
    user = get_object_or_404(Users, user_id=user_id)  # Get the user or return 404
    serializer = UserSerializer(user)  # Serialize the single instance to JSON
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def userExists(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Check if a user exists in the database by their user ID.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user to check.

    Returns:
        JsonResponse: A response indicating whether the user exists.
    """
    exists = Users.objects.filter(user_id=user_id).exists()  # Check if user exists

    if exists:
        return JsonResponse({"exists": True}, status=status.HTTP_200_OK)
    return JsonResponse({"exists": False}, status=status.HTTP_404_NOT_FOUND)