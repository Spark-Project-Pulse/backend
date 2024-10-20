from django.urls import path
from ..views import tag_views 

urlpatterns = [
    path('create/', tag_views.createTag, name='createTag'),
    path('getAll', tag_views.getAllTags, name='getAllTags'),
]
