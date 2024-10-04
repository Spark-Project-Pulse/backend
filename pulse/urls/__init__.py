# urls/__init__.py
# from django.contrib import admin
from django.urls import include, path

# In order to have seperate url files, django requires this file and to import the urls here:
from .question_urls import urlpatterns as question_urls
from .project_urls import urlpatterns as project_urls

# All URL routes
urlpatterns = [
    path('questions/', include(question_urls)),
    path('projects/', include(project_urls)),
]
