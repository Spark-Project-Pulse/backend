# urls/user_urls.py
from django.urls import path
from ..views import user_views

# URL routes for calls relating to users
urlpatterns = [
    path('create/', user_views.createUser, name='createUser'),
    path('getById/<str:user_id>/', user_views.getUserById, name='getUserById'),
    path('userExists/<str:user_id>/', user_views.userExists, name='getUserById'),
]
