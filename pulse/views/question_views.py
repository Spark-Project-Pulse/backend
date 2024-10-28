from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.postgres.search import SearchQuery, SearchRank
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from ..models import Questions
from ..serializers import QuestionSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import throttle_classes




@api_view(["POST"])
def createQuestion(request: HttpRequest) -> JsonResponse:
    """
    Create a question using the QuestionSerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.
    
    Returns:
        JsonResponse: A response with the created question's ID if successful,
        or validation errors if the data is invalid.
    """
    serializer = QuestionSerializer(data=request.data)  # Deserialize and validate the data
    if serializer.is_valid():
        question = serializer.save()  # Save the valid data as a new Question instance
        return JsonResponse(
            {"question_id": question.question_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getAllQuestions(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all questions from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A response containing serialized data for all questions.
    """
    questions = Questions.objects.all().order_by('-created_at')  # Retrieve all Question instances
    serializer = QuestionSerializer(questions, many=True)  # Serialize the queryset to JSON
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getQuestionsByUserId(request: HttpRequest, user_id: int) -> JsonResponse:
    """
    Retrieve all questions associated with a specific user_id
    from the database and serialize them to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The ID of the user whose questions are to be retrieved.

    Returns:
        JsonResponse: A response containing serialized data for the user's questions.
    """
    questions = Questions.objects.filter(asker_id=user_id).order_by('-created_at')  # Retrieve questions for the specified user
    serializer = QuestionSerializer(questions, many=True)  # Serialize the queryset to JSON
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getQuestionById(request: HttpRequest, question_id: str) -> JsonResponse:
    """
    Retrieve a single question by its ID and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        question_id (str): The ID of the question to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested question.
    """
    question = get_object_or_404(Questions, question_id=question_id)  # Get the question or return 404
    serializer = QuestionSerializer(question)  # Serialize the single instance to JSON
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class BurstUserRateThrottle(UserRateThrottle):
    rate = '10/min'

class BurstAnonRateThrottle(AnonRateThrottle):
    rate = '5/min'

@require_GET
@csrf_exempt 
@throttle_classes([BurstUserRateThrottle, BurstAnonRateThrottle])
def search_questions(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse(
            {"error": "No search query provided."},
            status=400
        )

    # Create the search query and annotate with rank
    search_query = SearchQuery(query, search_type="websearch")  # websearch for improved query syntax
    questions = Questions.objects.annotate(
        rank=SearchRank('search_vector', search_query)
    ).filter(search_vector=search_query).order_by('-rank', '-created_at')[:10]  # Limit to top 10

    # Serialize results
    serializer = QuestionSerializer(questions, many=True)
    response = {
        "results": serializer.data
    }
    
    return JsonResponse(response, status=200)