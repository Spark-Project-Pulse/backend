from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpRequest
from ..models import Badge, UserBadge, UserBadgeProgress, Answers
from ..serializers import BadgeSerializer, UserBadgeSerializer, UserBadgeProgressSerializer
from rest_framework import status
from django.db import connection

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
    Updates the progress for badges and ensures progress aligns with reputation and tier thresholds.
    """
    try:
        from django.db.models import Sum
        from django.utils import timezone
        import logging

        logger = logging.getLogger(__name__)

        badges = Badge.objects.all().prefetch_related('tiers', 'associated_tag')

        for badge in badges:
            # Determine user's relevant reputation
            reputation = user.reputation if badge.is_global else (
                Answers.objects.filter(
                    expert=user,
                    question__tags=badge.associated_tag
                )
                .aggregate(total_score=Sum("score"))
                .get("total_score") or 0
            )

            # Fetch qualifying tiers
            qualifying_tiers = badge.tiers.filter(
                reputation_threshold__lte=reputation
            ).order_by('-tier_level')
            highest_tier = qualifying_tiers.first()

            # Get next tier (if any)
            next_tier = badge.tiers.filter(
                reputation_threshold__gt=reputation
            ).order_by('reputation_threshold').first()

            # Award first tier or update existing badge
            user_badge, created = UserBadge.objects.get_or_create(
                user=user,
                badge=badge,
                defaults={
                    'badge_tier': highest_tier,
                    'earned_at': timezone.now(),
                }
            )
            if not created and highest_tier:
                if not user_badge.badge_tier or highest_tier.tier_level > user_badge.badge_tier.tier_level:
                    user_badge.badge_tier = highest_tier
                    user_badge.earned_at = timezone.now()
                    user_badge.save()

            # Update progress
            progress_target = max(
                (highest_tier.reputation_threshold if highest_tier else 0),
                (next_tier.reputation_threshold if next_tier else 0)
            )
            progress_value = max(reputation, user_badge.badge_tier.reputation_threshold if user_badge.badge_tier else 0)

            # Calculate if the badge is achieved
            is_achieved = progress_value >= (highest_tier.reputation_threshold if highest_tier else 0)

            progress, progress_created = UserBadgeProgress.objects.get_or_create(
                user=user,
                badge=badge,
                defaults={
                    'progress_value': progress_value,
                    'progress_target': progress_target,
                }
            )
            if not progress_created:
                progress.progress_value = progress_value
                progress.progress_target = progress_target
                progress.save()

            # Log whether the badge is achieved
            if is_achieved:
                logger.info(f"Badge '{badge.name}' is achieved for user '{user.username}'.")
            else:
                logger.info(f"User '{user.username}' is progressing towards badge '{badge.name}'.")

    except Exception as e:
        logger.error(f"Error in updateProgressAndAwardBadges for user {user.username}: {e}")
        raise
