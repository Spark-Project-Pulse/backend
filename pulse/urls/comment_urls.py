# urls/comment_urls.py
from django.urls import path
from ..views import comment_views

# URL routes for calls relating to comments
urlpatterns = [
    path('create/', comment_views.createComment, name='createComment'),
    path('getCommentsByAnswerId/<str:answer_id>/', comment_views.getCommentsByAnswerId, name='getCommentsByAnswerId'),
]
