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
from django.db.models import Count, Q
from uuid import UUID

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
    serializer = QuestionSerializer(
        data=request.data
    )  # Deserialize and validate the data
    if serializer.is_valid():
        question = serializer.save()  # Save the valid data as a new Question instance
        return JsonResponse(
            {"question_id": question.question_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getAllQuestions(request: HttpRequest) -> JsonResponse:
    """
    Retrieve questions from the database with pagination, optional tag filtering, and search functionality.
    """
    # Get query parameters
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    selected_tags = request.GET.getlist('tags')  # Expecting UUIDs like ?tags=uuid1&tags=uuid2
    search_query = request.GET.get('search', '').strip()

    # Start with all questions, ordered by creation date descending
    questions = Questions.objects.all()

    # Apply search filter if search_query is provided
    if search_query:
        search_vector = SearchQuery(search_query, search_type='websearch')
        questions = questions.annotate(
            rank=SearchRank('search_vector', search_vector)
        ).filter(search_vector=search_vector).order_by('-rank', '-created_at')
    else:
        questions = questions.order_by('-created_at')

    # Filter questions by tags if any tags are provided
    if selected_tags:
        # Convert tag IDs to UUID objects
        try:
            selected_tags = [UUID(tag_id) for tag_id in selected_tags]
        except ValueError:
            return JsonResponse({'error': 'Invalid tag IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        num_selected_tags = len(selected_tags)

        # Filter questions that have all of the selected tags
        questions = questions.filter(tags__tag_id__in=selected_tags)
        questions = questions.annotate(
            matching_tags=Count('tags', filter=Q(tags__tag_id__in=selected_tags), distinct=True)
        ).filter(matching_tags=num_selected_tags)

    # Remove duplicates
    questions = questions.distinct()

    # Pagination
    paginator = Paginator(questions, page_size)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = []

    serializer = QuestionSerializer(page_obj.object_list, many=True)
    response_data = {
        'questions': serializer.data,
        'totalQuestions': paginator.count,
        'totalPages': paginator.num_pages,
        'currentPage': page_number,
    }
    return JsonResponse(response_data, status=status.HTTP_200_OK)


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
    questions = Questions.objects.filter(asker_id=user_id).order_by(
        "-created_at"
    )  # Retrieve questions for the specified user
    serializer = QuestionSerializer(
        questions, many=True
    )  # Serialize the queryset to JSON
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
    question = get_object_or_404(
        Questions, question_id=question_id
    )  # Get the question or return 404
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
    tags = request.GET.getlist('tags')

    if not query and not tags:
        return JsonResponse(
            {"error": "No search query or tags provided."},
            status=400
        )

    search_query = SearchQuery(query, search_type="websearch") if query else None
    questions = Questions.objects.all()

    # Apply full-text search filter if there's a search query
    if search_query:
        questions = questions.annotate(
            rank=SearchRank('search_vector', search_query)
        ).filter(search_vector=search_query).order_by('-rank', '-created_at')

    if tags:
        questions = questions.filter(tags__name__in=tags).distinct()

    #Temporary: until pagination is implemented
    questions = questions[:10]

    serializer = QuestionSerializer(questions, many=True)
    return JsonResponse({"results": serializer.data}, status=200)
