# Generated by Django 5.1.2 on 2024-11-03 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0023_alter_communities_avatar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='related_community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulse.communities'),
        ),
    ]