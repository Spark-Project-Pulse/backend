# urls/user_urls.py
from django.urls import path
from ..views import user_views

# URL routes for calls relating to users
urlpatterns = [
    # POST Requests
    path('create/', user_views.createUser, name='createUser'),
    path('increaseReputationById/<str:user_id>/', user_views.increaseReputation, name='increaseReputationById'),
    
    # GET Requests
    path('getById/<str:user_id>/', user_views.getUserById, name='getUserById'),
    path('getByUsername/<str:username>/', user_views.getUserByUsername, name='getUserByUsername'),
    path('userExists/<str:user_id>/', user_views.userExists, name='getUserById'),
]
