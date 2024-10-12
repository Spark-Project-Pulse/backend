import uuid
from django.db import models

class Answers(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expert = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)  # Anonymize if user is deleted
    question = models.ForeignKey('Questions', on_delete=models.CASCADE, blank=True, null=True)  # Delete answer if question is deleted
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
    tags = models.ManyToManyField('Tags', related_name='projects')  # Many-to-Many with Tags

    class Meta:
        db_table = 'Projects'


class Questions(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asker = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    related_project = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', related_name='questions')  # Many-to-Many with Tags

    class Meta:
        db_table = 'Questions'


class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Tags'

    def __str__(self):
        return self.name #returns tag name instead of object id 


class Users(models.Model):
    user = models.OneToOneField('AuthUser', on_delete=models.CASCADE, primary_key=True, default=uuid.uuid4)
    username = models.TextField(unique=True)
    pfp_url = models.TextField(blank=True, null=True)
    reputation = models.BigIntegerField()

    class Meta:
        db_table = 'Users'


class AuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Add any other fields that are needed in the Supabase auth table

    class Meta:
        managed = False  # Indicating that Django should not manage this table
        db_table = 'auth"."users'
