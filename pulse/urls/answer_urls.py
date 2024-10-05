# urls/answer_urls.py
from django.urls import path
from ..views import answer_views

# URL routes for calls relating to answers
urlpatterns = [
    path('create/', answer_views.createAnswer, name='createAnswer'),
    path('getAnswersByQuestionId/<str:question_id>/', answer_views.getAnswersByQuestionId, name='getAnswersByQuestionId'),
]
