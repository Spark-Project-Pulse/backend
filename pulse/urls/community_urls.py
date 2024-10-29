# urls/community_urls.py
from django.urls import path
from ..views import community_views

# URL routes for calls relating to communities
urlpatterns = [
    path('create/', community_views.createCommunity, name='createComment'),
    path('getAll/', community_views.getAllCommunities, name='getAllCommunities'),
    path('getById/<str:community_id>/', community_views.getCommunityById, name='getCommunityById'),
]
