# urls/answer_urls.py
from django.urls import path
from ..views import answer_views

# URL routes for calls relating to answers
urlpatterns = [
    # POST Requests
    path('create/', answer_views.createAnswer, name='createAnswer'),
    path('upvote/', answer_views.upvoteAnswer, name='upvoteAnswer'),
    path('downvote/', answer_views.downvoteAnswer, name='downvoteAnswer'),
    
    # GET Requests
    path('getAnswersByQuestionId/<str:question_id>/', answer_views.getAnswersByQuestionId, name='getAnswersByQuestionId'),
    path('getAnswersByQuestionIdWithUser/<str:question_id>/<str:user_id>/', answer_views.getAnswersByQuestionIdWithUser, name='getAnswersByQuestionIdWithUser'),
]
