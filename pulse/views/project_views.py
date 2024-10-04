from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from ..serializers import ProjectSerializer

@api_view(["POST"])
def createProject(request: HttpRequest) -> JsonResponse:
    """
    Create a project using the ProjectSerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.
    
    Returns:
        JsonResponse: A response with the created project's ID if successful,
        or validation errors if the data is invalid.
    """
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save()
        return JsonResponse(
            {"project_id": project.project_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)