# Generated by Django 5.1.1 on 2024-10-02 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0004_alter_answers_answer_id_alter_answers_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.questions'),
        ),
    ]
