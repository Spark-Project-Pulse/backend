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

    # If the user has already upvoted, change vote to neutral
    if existing_vote and existing_vote.vote_type == 'upvote':
        existing_vote.delete()
        answer.score -= 1
        answer.save()
        return JsonResponse({"message": "Upvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)
    
    # If user has downvoted, switch to upvote
    if existing_vote and existing_vote.vote_type == 'downvote':
        existing_vote.delete()
        Votes.objects.create(user=user, answer=answer, vote_type='upvote')
        answer.score += 2  # Increment score by 2
        answer.save()
        return JsonResponse({"message": "Upvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

    # Record the upvote
    Votes.objects.create(user=user, answer=answer, vote_type='upvote')
    answer.score += 1  # Increment score by 1
    answer.save()

    # Return the updated vote count
    return JsonResponse({"message": "Upvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

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

    # If the user has already downvoted, change vote to neutral
    if existing_vote and existing_vote.vote_type == 'downvote':
        existing_vote.delete()
        answer.score += 1
        answer.save()
        return JsonResponse({"message": "Downvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)
    
    # If user has upvoted, switch to downvote
    if existing_vote and existing_vote.vote_type == 'upvote':
        existing_vote.delete()
        Votes.objects.create(user=user, answer=answer, vote_type='downvote')
        answer.score -= 2  # Decrement score by 2
        answer.save()
        return JsonResponse({"message": "Downvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

    # Record the downvote
    Votes.objects.create(user=user, answer=answer, vote_type='downvote')
    answer.score -= 1  # Decrement score by 1
    answer.save()

    # Return the updated vote count
    return JsonResponse({"message": "Downvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAnswersByQuestionId(request: HttpRequest, question_id: str) -> JsonResponse:
    # Retrieve all answers for the given question_id
    answers = Answers.objects.filter(question=question_id)
    
    # Serialize the list of answers, setting many=True to indicate multiple objects
    serializer = AnswerSerializer(answers, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAnswersByQuestionIdWithUser(request: HttpRequest, question_id: str, user_id: str) -> JsonResponse:
    # Retrieve all answers for the given question_id
    answers = Answers.objects.filter(question=question_id)
    
    # Serialize the list of answers, setting many=True to indicate multiple objects
    serialized_answers = AnswerSerializer(answers, many=True).data
    
    for answer in serialized_answers:
        # Get the votes for the current user on this answer
        user_vote = Votes.objects.filter(user_id=user_id, answer_id=answer['answer_id']).first()
        
        # Set the upvote/downvote flags based on the user's vote
        answer['curr_user_upvoted'] = user_vote.vote_type == 'upvote' if user_vote else False
        answer['curr_user_downvoted'] = user_vote.vote_type == 'downvote' if user_vote else False

    return JsonResponse(serialized_answers, safe=False, status=status.HTTP_200_OK)
