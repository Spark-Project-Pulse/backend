from django.urls import path
from ..views import badge_views

urlpatterns = [
    path('getAll/', badge_views.getAllBadges, name='getAllBadges'),  # get all badges
    path('getUserBadges/<uuid:user_id>/', badge_views.getUserBadges, name='getUserBadges'),  # get badges earned by user
    path('getUserProgress/<uuid:user_id>/', badge_views.getUserBadgeProgress, name='getUserBadgeProgress'),  # get user badge progress
]