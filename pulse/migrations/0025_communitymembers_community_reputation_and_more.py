# Generated by Django 5.1.2 on 2024-11-03 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0024_questions_related_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymembers',
            name='community_reputation',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='users',
            name='reputation',
            field=models.BigIntegerField(default=0),
        ),
    ]
