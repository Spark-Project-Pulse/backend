# urls/-roject_urls.py
from django.urls import path
from ..views import project_views

# URL routes for calls relating to projects
urlpatterns = [
    path('create/', project_views.createProject, name='createProject'),
    # path('getAll/', project_views.getAllProjects, name='getAllProjects'),
    # path('getById/<str:Project_id>/', project_views.getProjectById, name='getProjectById'),
]
