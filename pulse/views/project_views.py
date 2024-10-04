from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from ..models import Projects
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


@api_view(["GET"])
def getAllProjects(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all projects from the database and serialize them
    to JSON format.

    TODO: eventually this should have the ability to filter only projects for a specific person... or use other filters (e.g. tags)

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A response containing serialized data for all Project.
    """
    project = Projects.objects.all()
    serializer = ProjectSerializer(project, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getProjectById(request: HttpRequest, project_id: str) -> JsonResponse:
    """
    Retrieve a single project by its ID and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        project_id (str): The ID of the project to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested project.
    """
    project = get_object_or_404(Projects, project_id=project_id)
    serializer = ProjectSerializer(project)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)