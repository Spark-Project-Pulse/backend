# Generated by Django 5.1.2 on 2024-10-21 22:47

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0013_projects_repo_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('vote_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vote_type', models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.answers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.users')),
            ],
            options={
                'db_table': 'Votes',
                'unique_together': {('user', 'answer')},
            },
        ),
    ]