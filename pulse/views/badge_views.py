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
    Updates the badge progress for the user and awards badges if progress meets or exceeds the target.
    """
    from django.db.models import Sum

    # Get all available badges
    badges = Badge.objects.all()

    for badge in badges:
        if badge.is_global:
            # Update global badge progress
            progress, created = UserBadgeProgress.objects.get_or_create(
                user=user, badge=badge,
                defaults={"progress_value": 0, "progress_target": badge.reputation_threshold}
            )
            progress.progress_value = user.reputation
            progress.save()

            # Award badge if the progress meets or exceeds the target
            if progress.progress_value >= progress.progress_target:
                UserBadge.objects.get_or_create(user=user, badge=badge)

        else:
            # Calculate tag-specific reputation progress
            tag_reputation = (
                Answers.objects.filter(
                    expert=user,
                    question__tags__id=badge.associated_tag_id
                )
                .aggregate(total_score=Sum("score"))
                .get("total_score", 0)
            )

            progress, created = UserBadgeProgress.objects.get_or_create(
                user=user, badge=badge,
                defaults={"progress_value": 0, "progress_target": badge.reputation_threshold}
            )
            progress.progress_value = tag_reputation or 0
            progress.save()

            # Award badge if the progress meets or exceeds the target
            if progress.progress_value >= progress.progress_target:
                UserBadge.objects.get_or_create(user=user, badge=badge)
