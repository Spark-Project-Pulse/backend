# urls/question_urls.py
from django.urls import path
from ..views import question_views

# URL routes for calls relating to questions
urlpatterns = [
    path('create/', question_views.createQuestion, name='createQuestion'),
    path('getAll/', question_views.getAllQuestions, name='getAllQuestions'),
    path('getById/<str:question_id>/', question_views.getQuestionById, name='getQuestionById'),
]
