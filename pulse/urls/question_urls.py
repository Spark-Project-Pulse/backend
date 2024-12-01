# urls/question_urls.py
from django.urls import path
from ..views import question_views

# URL routes for calls relating to questions
urlpatterns = [
    path('create/', question_views.createQuestion, name='createQuestion'),
    path('getAll/', question_views.getAllQuestions, name='getAllQuestions'),
    path('getByUserId/<str:user_id>/', question_views.getQuestionsByUserId, name='getQuestionsByUserId'),
    path('getById/<str:question_id>/', question_views.getQuestionById, name='getQuestionById'),
    path('search/', question_views.searchQuestions, name='search_questions'),
    path('changeMark/<str:question_id>/', question_views.changeMark, name='changeMark'),
    path('update/<str:question_id>/', question_views.updateQuestion, name='updateQuestion'),
    path('delete/<str:question_id>/', question_views.deleteQuestion, name='deleteQuestion'),
]
