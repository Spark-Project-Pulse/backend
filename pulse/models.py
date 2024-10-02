import uuid
from django.db import models


class Answers(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expert = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Answers'


class Projects(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    public = models.BooleanField()
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Projects'


class Questions(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asker = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    related_project = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Questions'


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.TextField(unique=True)
    pfp_url = models.TextField(blank=True, null=True)
    reputation = models.BigIntegerField()

    class Meta:
        db_table = 'Users'

