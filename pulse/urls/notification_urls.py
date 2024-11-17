from django.urls import path
from ..views import notification_views 

urlpatterns = [
    path('getByUserId/<str:user_id>/', notification_views.getNotificationsByUserId, name='getNotificationsByUserId'),
    path('getCountByUserId/<str:user_id>/', notification_views.getNotificationsCountByUserId, name='getNotificationsCountByUserId'),

    path('markAsRead/<str:user_id>/<str:notification_id>', notification_views.markAsRead, name='markAsReadByUserId'),
    path('markAsUnread/<str:user_id>/<str:notification_id>', notification_views.markAsUnread, name='markAsUnreadByUserId'),
    path('delete/<str:user_id>/<str:notification_id>', notification_views.deleteNotification, name='deleteNotification'),
]
