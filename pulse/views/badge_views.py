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
    Updates the progress for badges and awards badges with specific tiers if criteria are met.
    """
    try:
        from django.db.models import Sum
        from django.utils import timezone
        import logging

        logger = logging.getLogger(__name__)

        # Fetch all badges with their related tiers and associated tags
        badges = Badge.objects.all().prefetch_related('tiers', 'associated_tag')

        for badge in badges:
            # Determine the user's relevant reputation for the badge
            if badge.is_global:
                # For global badges, use the user's total reputation
                reputation = user.reputation
            else:
                # For tag-specific badges, calculate reputation from answers with the associated tag
                if badge.associated_tag:
                    tag_reputation = (
                        Answers.objects.filter(
                            expert=user,
                            question__tags=badge.associated_tag
                        )
                        .aggregate(total_score=Sum("score"))
                        .get("total_score") or 0
                    )
                    reputation = tag_reputation
                else:
                    # If the badge has no associated tag, skip it
                    logger.warning(f"Badge '{badge.name}' has no associated tag and is not global.")
                    continue

            # Get all badge tiers the user qualifies for
            qualifying_tiers = badge.tiers.filter(
                reputation_threshold__lte=reputation
            ).order_by('-tier_level')

            if qualifying_tiers.exists():
                highest_tier = qualifying_tiers.first()

                # Check if the user already has this badge
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=badge,
                    defaults={
                        'badge_tier': highest_tier,
                        'earned_at': timezone.now(),
                    }
                )
                if not created:
                    # Check if the user's badge tier needs to be upgraded
                    current_tier_level = user_badge.badge_tier.tier_level
                    if highest_tier.tier_level > current_tier_level:
                        # Upgrade the badge tier
                        user_badge.badge_tier = highest_tier
                        user_badge.earned_at = timezone.now()
                        user_badge.save()
                        logger.info(f"Upgraded badge '{badge.name}' to tier '{highest_tier.name}' for user '{user.username}'.")
                else:
                    logger.info(f"Awarded badge '{badge.name}' with tier '{highest_tier.name}' to user '{user.username}'.")
            else:
                # User hasn't qualified for any tier yet; optionally handle progress tracking
                pass

            # Determine progress towards the next tier
            next_tier = badge.tiers.filter(
                reputation_threshold__gt=reputation
            ).order_by('reputation_threshold').first()

            progress_target = next_tier.reputation_threshold if next_tier else None

            # Update or create UserBadgeProgress
            progress, created = UserBadgeProgress.objects.get_or_create(
                user=user,
                badge=badge,
                defaults={
                    'progress_value': reputation,
                    'progress_target': progress_target,
                }
            )
            if not created:
                progress.progress_value = reputation
                progress.progress_target = progress_target
                progress.save()
                logger.info(f"Updated progress for badge '{badge.name}' for user '{user.username}'.")

    except Exception as e:
        # Log the exception for debugging
        logger.error(f"Error in updateProgressAndAwardBadges for user {user.username}: {e}")
        raise