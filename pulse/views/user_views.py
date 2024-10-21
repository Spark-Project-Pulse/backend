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

@api_view(["POST"])
def increaseReputation(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Increase the reputation of a user by 1, identified by their user ID.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user whose reputation should be increased.

    Returns:
        JsonResponse: A response indicating the new reputation or an error message.
    """
    try:
        user = get_object_or_404(Users, user_id=user_id)  # Retrieve the user by ID
        user.reputation += 1  # Increment the reputation
        user.save()  # Save the updated user object
        return JsonResponse(
            {"user_id": user.user_id, "new_reputation": user.reputation},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return JsonResponse(
            {"error": "Unable to increase reputation", "details": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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
def getUserByUsername(request: HttpRequest, username: str) -> JsonResponse:
    """
    Retrieve a single user by their username and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        username (str): The username of the user to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested user.
    """
    user = get_object_or_404(Users, username=username)  # Get the user or return 404
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
    try:
        exists = Users.objects.filter(user_id=user_id).exists()  # Check if the user exists
        return JsonResponse({"exists": exists}, status=status.HTTP_200_OK)  # Return a 200 OK response with a boolean result
    except Exception as e:
        return JsonResponse(
            {"error": "An error occurred", "details": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )  # Log the error and return a 500 response for unexpected errors
        