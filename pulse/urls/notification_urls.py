from django.urls import path
from ..views import notification_views 

urlpatterns = [
    path('getAll/', notification_views.getAllNotifications, name='getAllNotifications'),
]
