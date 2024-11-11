from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Tags
from rest_framework import status
from ..serializers import TagSerializer

@api_view(["POST"])
def createTag(request: HttpRequest) -> JsonResponse:
    """
    Create a tag using the TagSerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.
    
    Returns:
        JsonResponse: A response with the created tag's data if successful,
        or validation errors if the data is invalid.
    """
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        tag = serializer.save()
        return JsonResponse(
            {"tag_id": tag.tag_id}, status=status.HTTP_201_CREATED
        )

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getAllTags(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all tags from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        Json
    """
    tags = Tags.objects.all()
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
