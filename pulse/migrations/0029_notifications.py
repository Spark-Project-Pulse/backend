# Generated by Django 5.1.2 on 2024-11-10 20:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0028_merge_20241104_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('notification_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notification_type', models.CharField(choices=[('new_answer', 'New Answer'), ('new_comment', 'New Comment'), ('answer_accepted', 'Answer Accepted'), ('mention', 'Mention'), ('vote', 'Vote Received')], max_length=20)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications_triggered', to='pulse.users')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.answers')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.comments')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.questions')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='pulse.users')),
            ],
            options={
                'db_table': 'Notifications',
                'indexes': [models.Index(fields=['recipient', '-created_at'], name='Notificatio_recipie_fca97d_idx'), models.Index(fields=['recipient', 'read'], name='Notificatio_recipie_363fe4_idx')],
            },
        ),
    ]
