# urls/question_urls.py
from django.urls import path
from ..views.question_views import (
    getAllQuestions
)

# ULR routes for calls relating to questions
urlpatterns = [
    path('', getAllQuestions, name='getAllQuestions')
]
