from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..models import Answers, Votes, Users
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
        serialized_answer = AnswerSerializer(answer)  # Serialize the saved answer
        return JsonResponse(serialized_answer.data, status=status.HTTP_201_CREATED)  # Return the serialized data

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def upvoteAnswer(request: HttpRequest) -> JsonResponse:
    """
    Upvote an answer, increasing its score by 1.
    If the user has already downvoted, switch to upvote.

    Args:
        request (HttpRequest): The incoming HTTP request containing user_id and answer_id.

    Returns:
        JsonResponse: The updated score or an error message.
    """
    user_id = request.data.get('user_id')
    answer_id = request.data.get('answer_id')

    user = get_object_or_404(Users, pk=user_id)
    answer = get_object_or_404(Answers, pk=answer_id)

    # Check if the user has already upvoted
    existing_vote = Votes.objects.filter(user=user, answer=answer).first()

    if existing_vote and existing_vote.vote_type == 'upvote':
        return JsonResponse({"error": "User has already upvoted this answer"}, status=status.HTTP_400_BAD_REQUEST)
    
    # If user has downvoted, switch to upvote
    if existing_vote and existing_vote.vote_type == 'downvote':
        existing_vote.delete()

    # Record the upvote
    Votes.objects.create(user=user, answer=answer, vote_type='upvote')

    # Return the updated vote count
    new_score = answer.votes_set.filter(vote_type='upvote').count() - answer.votes_set.filter(vote_type='downvote').count()
    return JsonResponse({"message": "Upvote successful", "new_score": new_score}, status=status.HTTP_200_OK)

@api_view(["POST"])
def downvoteAnswer(request: HttpRequest) -> JsonResponse:
    """
    Downvote an answer, decreasing its score by 1.
    If the user has already upvoted, switch to downvote.

    Args:
        request (HttpRequest): The incoming HTTP request containing user_id and answer_id.

    Returns:
        JsonResponse: The updated score or an error message.
    """
    user_id = request.data.get('user_id')
    answer_id = request.data.get('answer_id')

    user = get_object_or_404(Users, pk=user_id)
    answer = get_object_or_404(Answers, pk=answer_id)

    # Check if the user has already downvoted
    existing_vote = Votes.objects.filter(user=user, answer=answer).first()

    if existing_vote and existing_vote.vote_type == 'downvote':
        return JsonResponse({"error": "User has already downvoted this answer"}, status=status.HTTP_400_BAD_REQUEST)
    
    # If user has upvoted, switch to downvote
    if existing_vote and existing_vote.vote_type == 'upvote':
        existing_vote.delete()

    # Record the downvote
    Votes.objects.create(user=user, answer=answer, vote_type='downvote')

    # Return the updated vote count
    new_score = answer.votes_set.filter(vote_type='upvote').count() - answer.votes_set.filter(vote_type='downvote').count()
    return JsonResponse({"message": "Downvote successful", "new_score": new_score}, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAnswersByQuestionId(request: HttpRequest, question_id: str) -> JsonResponse:
    # Retrieve all answers for the given question_id
    answers = Answers.objects.filter(question=question_id)
    
    # Serialize the list of answers, setting many=True to indicate multiple objects
    serializer = AnswerSerializer(answers, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
