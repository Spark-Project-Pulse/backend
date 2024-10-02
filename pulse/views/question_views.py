from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..models import Questions
from ..serializers import QuestionSerializer


@api_view(["POST"])
def createQuestion(request: HttpRequest) -> JsonResponse:
    """Create a question

    Returns:
        JsonResponse:
    """
    serializer = QuestionSerializer(data=request.data)  # Use request.data for DRF (djang-rest-framework) compatibility
    if serializer.is_valid():
        question = serializer.save()  # Save the new question
        return JsonResponse(
            {"question_id": question.question_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getAllQuestions(request: HttpRequest) -> JsonResponse:
    questions = Questions.objects.all()  # Get all questions
    serializer = QuestionSerializer(questions, many=True)  # Serialize the queryset
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getQuestionById(request: HttpRequest, question_id: str) -> JsonResponse:
    question = get_object_or_404(Questions, question_id=question_id)  # Get the question or return 404
    serializer = QuestionSerializer(question)  # Serialize the single instance
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)