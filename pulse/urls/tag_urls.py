from django.urls import path
from ..views import tag_views 

urlpatterns = [
    path('', tag_views.get_all_tags, name='get_all_tags'),  # Accessible at /tags/
]
