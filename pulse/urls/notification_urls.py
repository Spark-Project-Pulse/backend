from django.urls import path
from ..views import notification_views 

urlpatterns = [
    path('getAll/', notification_views.getAllNotifications, name='getAllNotifications'),
    path('getByUserId/<str:user_id>/', notification_views.getNotificationsByUserId, name='getNotificationsByUserId'),
    path('markAsRead/<str:user_id>/<str:notification_id>', notification_views.markAsRead, name='markAsReadByUserId'),
]
