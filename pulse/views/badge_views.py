from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Badge, UserBadge, UserBadgeProgress, Answers
from ..serializers import BadgeSerializer, UserBadgeSerializer, UserBadgeProgressSerializer
from rest_framework import status

@api_view(["GET"])
def getAllBadges(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all badges from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A response containing serialized data for all badges.
    """
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserBadges(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve all badges earned by a specific user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user.

    Returns:
        JsonResponse: A response containing serialized data for the user's badges.
    """
    user_badges = UserBadge.objects.filter(user_id=user_id)
    serializer = UserBadgeSerializer(user_badges, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserBadgeProgress(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve badge progress for a specific user.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user.

    Returns:
        JsonResponse: A response containing serialized data for the user's badge progress.
    """
    progress = UserBadgeProgress.objects.filter(user_id=user_id)
    serializer = UserBadgeProgressSerializer(progress, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

def updateProgressAndAwardBadges(user):
    """
    Updates the progress for badges and awards badges if criteria are met.
    """
    try:
        from django.db.models import Sum

        # Fetch all badges
        badges = Badge.objects.all()

        for badge in badges:
            if badge.is_global:
                # Update global badge progress
                progress, created = UserBadgeProgress.objects.get_or_create(
                    user=user,
                    badge=badge,
                    defaults={
                        'progress_value': user.reputation,
                        'progress_target': badge.reputation_threshold,
                    }
                )
                if not created:
                    progress.progress_value = user.reputation
                    progress.save()

                # Check if the badge should be awarded
                if user.reputation >= badge.reputation_threshold:
                    UserBadge.objects.get_or_create(user=user, badge=badge)
            else:
                # Calculate tag-specific reputation
                tag_reputation = (
                    Answers.objects.filter(
                        expert=user,
                        question__tags=badge.associated_tag
                    )
                    .aggregate(total_score=Sum("score"))
                    .get("total_score", 0)
                )
                progress, created = UserBadgeProgress.objects.get_or_create(
                    user=user,
                    badge=badge,
                    defaults={
                        'progress_value': tag_reputation,
                        'progress_target': badge.reputation_threshold,
                    }
                )
                if not created:
                    progress.progress_value = tag_reputation
                    progress.save()

                # Check if the badge should be awarded
                if tag_reputation >= badge.reputation_threshold:
                    UserBadge.objects.get_or_create(user=user, badge=badge)

    except Exception as e:
        # Log the exception for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in updateProgressAndAwardBadges for user {user.user}: {e}")
        raise