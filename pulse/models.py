import uuid
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# Things to note:
# 1. when using ForeignKey rels, Django's ORM automatically appends _id to the end of the field name (e.g. expert -> expert_id) in supabase
#   (you should NOT include _id manually at the end of any ForeignKey names)

# 2. however, when using PrimaryKeys (e.g. answer_id), you SHOULD include _id at the end of the field name (this is the standard in Django)

# 2. make sure you ONLY make changes to the database schema by editing this file (not the supabase dashboard), then push those changes using:
#    python manage.py makemigrations
#    python manage.py migrate

class Answers(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expert = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)  # don't delete answer if user is removed (just make anon)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE, blank=True, null=True)  # should delete answer if question is deleted
    score = models.BigIntegerField(default=0)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Answers'
        
class Votes(models.Model):
    # Vote choices for vote type
    VOTE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ] 

    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)  # Link to the user who voted
    answer = models.ForeignKey('Answers', on_delete=models.CASCADE)  # Link to the answer being voted on
    vote_type = models.CharField(max_length=8, choices=VOTE_CHOICES)  # Upvote or Downvote
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Votes'
        unique_together = ('user', 'answer')

class Projects(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    public = models.BooleanField()
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    repo_full_name = models.TextField(null=True)
    tags = models.ManyToManyField('Tags', related_name='projects', blank=True)  # Many-to-Many with Tags

    class Meta:
        db_table = 'Projects'


class Questions(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asker = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)
    related_project = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True)
    code_context = models.TextField(blank=True, null=True)
    code_context_full_pathname = models.TextField(blank=True, null=True)
    code_context_line_number = models.IntegerField(blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tags', related_name='questions', blank=True) # Many-to-Many with Tags

    search_vector = SearchVectorField(null=True, blank=True) #search

    class Meta:
        db_table = 'Questions'
        indexes = [
            GinIndex(fields=['search_vector']),  # Create a GIN index on the search_vector field
        ]


class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Tags'


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
    
class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expert = models.ForeignKey('Users', on_delete=models.SET_NULL, blank=True, null=True)               # don't delete comment if user is removed (just make anon)
    answer = models.ForeignKey('Answers', on_delete=models.CASCADE, blank=True, null=True)          # should delete comment if answer is deleted
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'
