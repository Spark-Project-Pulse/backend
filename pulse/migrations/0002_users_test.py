# Generated by Django 5.1.1 on 2024-10-02 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='test',
            field=models.TextField(blank=True, null=True),
        ),
    ]
