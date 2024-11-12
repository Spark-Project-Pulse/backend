# Generated by Django 5.1.3 on 2024-11-11 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0029_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notification_type',
            field=models.CharField(choices=[('question_answered', 'New Answer'), ('answer_commented', 'New Comment'), ('question_upvoted', 'Answer Accepted'), ('answer_accepted', 'Mention'), ('mention', 'Vote Received')], max_length=20),
        ),
    ]
