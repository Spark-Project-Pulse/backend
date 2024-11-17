from django.urls import path
from ..views import badge_views

# URL routes for calls relating to badges
urlpatterns = [
    path('getAll/', badge_views.getAllBadges, name='getAllBadges'),  # Get all badges
    path('getUserBadges/<uuid:user_id>/', badge_views.getUserBadges, name='getUserBadges'),  # Get badges earned by user
    path('getUserProgress/<uuid:user_id>/', badge_views.getUserBadgeProgress, name='getUserBadgeProgress'),  # Get user badge progress
]
