# urls/hive_urls.py
from django.urls import path
from ..views import hive_views

# URL routes for calls relating to hives
urlpatterns = [
    # POST Requests
    path('createRequest/', hive_views.createHiveRequest, name='createHiveRequest'),
    path('approveHiveRequest/', hive_views.approveHiveRequest, name='approveHiveRequest'),
    path('rejectHiveRequest/', hive_views.rejectHiveRequest, name='rejectHiveRequest'),
    path('addHiveMember/', hive_views.addHiveMember, name='addHiveMember'),
    path('removeHiveMember/', hive_views.removeHiveMember, name='removeHiveMember'),
    
    # GET Requests
    path('getAll/', hive_views.getAllHives, name='getAllHives'),
    path('getAllOptions/', hive_views.getAllHiveOptions, name='getAllHiveOptions'),
    path('getAllMembers/<str:hive_id>/', hive_views.getAllHiveMembers, name='getAllHiveMembers'),
    path('getById/<str:hive_id>/', hive_views.getHiveById, name='getHiveById'),
    path('getByTitle/<str:title>/', hive_views.getHiveByTitle, name='getHiveByTitle'),
    path('getUserHivesById/<str:user_id>/', hive_views.getUserHivesById, name='getUserHivesById'),
    path('getAllHiveRequests/', hive_views.getAllHiveRequests, name='getAllHiveRequests'),
    path('userIsPartOfHive/<str:title>/<str:user_id>/', hive_views.userIsPartOfHive, name='userIsPartOfHive'),
    path('search/', hive_views.searchHives, name='searchHives'),
]
