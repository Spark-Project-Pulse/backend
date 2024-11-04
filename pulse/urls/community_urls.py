# urls/community_urls.py
from django.urls import path
from ..views import community_views

# URL routes for calls relating to communities
urlpatterns = [
    # POST Requests
    path('create/', community_views.createCommunity, name='createComment'),
    path('addCommunityMember/', community_views.addCommunityMember, name='addCommunityMember'),
    path('removeCommunityMember/', community_views.removeCommunityMember, name='removeCommunityMember'),
    
    # GET Requests
    path('getAll/', community_views.getAllCommunities, name='getAllCommunities'),
    path('getById/<str:community_id>/', community_views.getCommunityById, name='getCommunityById'),
    path('getByTitle/<str:title>/', community_views.getCommunityByTitle, name='getCommunityByTitle'),
    path('userIsPartOfCommunity/<str:title>/<str:user_id>/', community_views.userIsPartOfCommunity, name='userIsPartOfCommunity'),
]
