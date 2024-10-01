# urls/question_urls.py
from django.urls import path
from ..views import question_views

# URL routes for calls relating to questions
urlpatterns = [
    path('getAll/', question_views.getAllQuestions, name='getAllQuestions'),
    path('create/', question_views.createQuestion, name='createQuestion'),
]
