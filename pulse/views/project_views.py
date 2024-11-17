from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from ..models import Projects
from ..serializers import ProjectSerializer
from services.ai_model_service import generate_code_review

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

@api_view(["POST"])
def codeReview(request: HttpRequest) -> JsonResponse:
    """
    Perform a code review on the provided code file and return suggestions.

    Args:
        request (HttpRequest): The incoming HTTP request containing the code details.

    Request Body:
        - project_title (str): Title of the project.
        - project_description (str): Description of the project.
        - file_name (str): Name of the file to review.
        - file_content (str): Content of the file to review.

    Returns:
        JsonResponse: Suggestions for code improvements or an error message.
    """
    try:
        # Extract required fields from request data
        project_title = request.data.get('project_title')
        project_description = request.data.get('project_description')
        file_name = request.data.get('file_name')
        file_content = request.data.get('file_content')

        # Validate inputs
        if not all([project_title, project_description, file_name, file_content]):
            return JsonResponse(
                {"error": "Missing required fields: project_title, project_description, file_name, or file_content"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the AI model for code review
        suggestions = generate_code_review(project_title, project_description, file_name, file_content)
        print(suggestions)

        # Return suggestions
        if suggestions:
            return JsonResponse(
                {"suggestions": suggestions},
                status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"error": "No suggestions returned."},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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
def getProjectsByUserId(request: HttpRequest, user_id: int) -> JsonResponse:
    """
    Retrieve all projects associated with a specific user_id
    from the database and serialize them to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The ID of the user whose projects are to be retrieved.

    Returns:
        JsonResponse: A response containing serialized data for the user's projects.
    """
    projects = Projects.objects.filter(owner_id=user_id).order_by('-created_at')  # Retrieve projects for the specified user
    serializer = ProjectSerializer(projects, many=True)  # Serialize the queryset to JSON
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