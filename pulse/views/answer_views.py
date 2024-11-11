from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..supabase_utils import check_content
from ..models import Answers, CommunityMembers, Votes, Users
from ..serializers import AnswerSerializer
from services.notification_service import NotificationService

'''----- POST REQUESTS -----'''

@api_view(["POST"])
def createAnswer(request: HttpRequest) -> JsonResponse:
    """
    Create an answer and increment contributions if the user is a member of the related community.
    
    Returns:
        JsonResponse:
    """
    serializer = AnswerSerializer(data=request.data)  # Use request.data for DRF compatibility
    if serializer.is_valid():
        # Content moderation
        response_text = request.data['response']
        if check_content(response_text):
            return JsonResponse({"toxic": True}, status=status.HTTP_400_BAD_REQUEST)
        
        answer: Answers = serializer.save()  # Save the new answer

        NotificationService.handle_new_answer(answer) # Handle notifications

        # Check if the question has a related community
        question = answer.question
        if question.related_community and answer.expert:
            community = question.related_community
            user = answer.expert

            # Check if the user is a member of the community
            try:
                community_member = CommunityMembers.objects.get(community=community, user=user)
                
                # Increment contributions if the user is a member
                community_member.contributions += 1
                community_member.save()
            except CommunityMembers.DoesNotExist:
                # If the user is not a member, do nothing
                pass

        serialized_answer = AnswerSerializer(answer)  # Serialize the saved answer
        return JsonResponse(serialized_answer.data, status=status.HTTP_201_CREATED)  # Return the serialized data

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def upvoteAnswer(request: HttpRequest) -> JsonResponse:
    user_id = request.data.get('user_id')
    answer_id = request.data.get('answer_id')

    user = get_object_or_404(Users, pk=user_id)
    answer = get_object_or_404(Answers, pk=answer_id)
    question = answer.question

    # Check if the user has already upvoted or downvoted
    existing_vote = Votes.objects.filter(user=user, answer=answer).first()

    # Handle upvote and reputation adjustments
    if existing_vote and existing_vote.vote_type == 'upvote':
        existing_vote.delete()
        answer.score -= 1
        answer.save()
        adjust_community_reputation(answer, question, -1)
        return JsonResponse({"message": "Upvote removed", "new_score": answer.score}, status=status.HTTP_200_OK)
    
    if existing_vote and existing_vote.vote_type == 'downvote':
        existing_vote.delete()
        Votes.objects.create(user=user, answer=answer, vote_type='upvote')
        answer.score += 2
        answer.save()
        adjust_community_reputation(answer, question, 2)
        return JsonResponse({"message": "Vote switched to upvote", "new_score": answer.score}, status=status.HTTP_200_OK)

    # Record a new upvote
    Votes.objects.create(user=user, answer=answer, vote_type='upvote')
    answer.score += 1
    answer.save()
    adjust_community_reputation(answer, question, 1)
    return JsonResponse({"message": "Upvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

@api_view(["POST"])
def downvoteAnswer(request: HttpRequest) -> JsonResponse:
    user_id = request.data.get('user_id')
    answer_id = request.data.get('answer_id')

    user = get_object_or_404(Users, pk=user_id)
    answer = get_object_or_404(Answers, pk=answer_id)
    question = answer.question  # Get the related question

    # Check if the user has already downvoted or upvoted
    existing_vote = Votes.objects.filter(user=user, answer=answer).first()

    # Handle downvote and reputation adjustments
    if existing_vote and existing_vote.vote_type == 'downvote':
        existing_vote.delete()
        answer.score += 1
        answer.save()
        adjust_community_reputation(answer, question, 1)
        return JsonResponse({"message": "Downvote removed", "new_score": answer.score}, status=status.HTTP_200_OK)

    if existing_vote and existing_vote.vote_type == 'upvote':
        existing_vote.delete()
        Votes.objects.create(user=user, answer=answer, vote_type='downvote')
        answer.score -= 2
        answer.save()
        adjust_community_reputation(answer, question, -2)
        return JsonResponse({"message": "Vote switched to downvote", "new_score": answer.score}, status=status.HTTP_200_OK)

    # Record a new downvote
    Votes.objects.create(user=user, answer=answer, vote_type='downvote')
    answer.score -= 1
    answer.save()
    adjust_community_reputation(answer, question, -1)
    return JsonResponse({"message": "Downvote successful", "new_score": answer.score}, status=status.HTTP_200_OK)

'''----- GET REQUESTS -----'''

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

'''----- HELPER FUNCTIONS -----'''

def adjust_community_reputation(answer, question, reputation_change):
    """
    Adjusts the community reputation of the answer's author based on the reputation change value
    only if they are already a member of the community.
    """
    # Check if the question is related to a community and the answer's author is defined
    if question.related_community and answer.expert:
        community = question.related_community
        user = answer.expert

        # Check if the user is already a member of the community
        try:
            community_member = CommunityMembers.objects.get(community=community, user=user)
            
            # Update the community reputation if the user is a member
            community_member.community_reputation += reputation_change
            community_member.save()
        except CommunityMembers.DoesNotExist:
            # If the user is not a member of the community, do nothing
            pass
