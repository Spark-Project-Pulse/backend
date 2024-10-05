from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..models import Answers
from ..serializers import AnswerSerializer


@api_view(["POST"])
def createAnswer(request: HttpRequest) -> JsonResponse:
    """Create an answer

    Returns:
        JsonResponse:
    """
    serializer = AnswerSerializer(data=request.data)  # Use request.data for DRF (djang-rest-framework) compatibility
    if serializer.is_valid():
        answer = serializer.save()  # Save the new answer
        return JsonResponse(
            {"answer_id": answer.answer_id,
             "response": answer.response}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getAnswersByQuestionId(request: HttpRequest, question_id: str) -> JsonResponse:
    # Retrieve all answers for the given question_id
    answers = Answers.objects.filter(question=question_id)
    
    # Serialize the list of answers, setting many=True to indicate multiple objects
    serializer = AnswerSerializer(answers, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)