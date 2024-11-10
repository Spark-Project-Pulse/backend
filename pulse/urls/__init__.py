# urls/__init__.py
# from django.contrib import admin
from django.urls import include, path

# In order to have seperate url files, django requires this file and to import the urls here:
from .answer_urls import urlpatterns as answer_urls
from .project_urls import urlpatterns as project_urls
from .question_urls import urlpatterns as question_urls
from .user_urls import urlpatterns as user_urls
from .tag_urls import urlpatterns as tag_urls
from .comment_urls import urlpatterns as comment_urls
from .community_urls import urlpatterns as community_urls
from .notification_urls import urlpatterns as notification_urls

# All URL routes
urlpatterns = [
    path('answers/', include(answer_urls)),
    path('projects/', include(project_urls)),
    path('questions/', include(question_urls)),
    path('users/', include(user_urls)),
    path('tags/', include (tag_urls)),
    path('comments/', include(comment_urls)),
    path('communities/', include(community_urls)),
    path('notifications/', include(notification_urls)),
]
