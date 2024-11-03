from django.conf import settings
from supabase import create_client, Client
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
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

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def create_bucket_if_not_exists(bucket_name):
    # Check if the bucket exists
    buckets = supabase.storage.list_buckets()

    # Check if the response is successful and get the list of buckets
    if isinstance(buckets, list): 

        # Get all bucket names
        bucket_names = [bucket.name for bucket in buckets]

        # Check if the specified bucket already exists
        if bucket_name in bucket_names:
            print(f"Bucket '{bucket_name}' already exists.")
        else:
            # Create the bucket since it doesn't exist
            try:
                response = supabase.storage.create_bucket(bucket_name)
                if 'error' in response:
                    print(f"Error creating bucket: {response['error']}")
                    return False
                else:
                    print(f"Bucket '{bucket_name}' created successfully.")
                return True
            except Exception as e:
                print("Error creating bucket: ", e)
                return False       
    else:
        print(f"Unexpected response format: {buckets}")
    
    return True

@api_view(["PUT"])
@parser_classes([MultiPartParser])  # To handle file uploads
def updateProfileImageById(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Updates the specified user's profile image

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user to update profile image on

    Returns:
        JsonResponse: A response containing serialized data for the requested user.
    """
    # Get the user or return 404
    user = get_object_or_404(Users, user_id=user_id)  

    # Get image file from request
    image_file = request.FILES.get('profile_image')
    if not image_file:
        return JsonResponse({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
    image_content = image_file.read()

    # Create bucket if it does not exist
    if not create_bucket_if_not_exists('profile-images'):
        return JsonResponse({'error': 'Could not ensure bucket exists.'}, status=500)
    
    # Set the upload path in Supabase Storage
    upload_path = f"{user_id}/profile-image"

    # Upload the image file to Supabase Storage, replaces current profile pic if it exists
    response = supabase.storage.from_("profile-images").upload(
        file=image_content, 
        path=upload_path, 
        file_options={"content-type": image_file.content_type, "upsert": "true"},
        )

    if response.status_code == 200:
        # Store the image URL in the user's profile

        user.profile_image_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/profile-images/{upload_path}"
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Failed to upload image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)