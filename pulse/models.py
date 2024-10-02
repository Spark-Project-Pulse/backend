# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answers(models.Model):
    answer_id = models.UUIDField(primary_key=True)
    expert = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    response = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'Answers'


class Projects(models.Model):
    project_id = models.UUIDField(primary_key=True)
    owner = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    public = models.BooleanField()
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'Projects'


class Questions(models.Model):
    question_id = models.UUIDField(primary_key=True)
    asker = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    related_project = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'Questions'


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True)
    username = models.TextField(unique=True)
    pfp_url = models.TextField(blank=True, null=True)
    reputation = models.BigIntegerField()

    class Meta:
        db_table = 'Users'

