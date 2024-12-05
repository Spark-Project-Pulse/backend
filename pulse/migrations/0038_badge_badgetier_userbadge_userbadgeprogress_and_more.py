# Generated by Django 5.1.3 on 2024-12-04 14:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0037_alter_questions_is_answered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('badge_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('is_global', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.URLField(blank=True, default='https://cdn-icons-png.flaticon.com/512/20/20100.png', null=True)),
                ('associated_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='badges', to='pulse.tags')),
            ],
            options={
                'db_table': 'Badges',
            },
        ),
        migrations.CreateModel(
            name='BadgeTier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tier_level', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('reputation_threshold', models.PositiveIntegerField()),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiers', to='pulse.badge')),
            ],
            options={
                'db_table': 'BadgeTier',
                'ordering': ['badge', 'tier_level'],
            },
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.badge')),
                ('badge_tier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pulse.badgetier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.users')),
            ],
            options={
                'db_table': 'UserBadges',
            },
        ),
        migrations.CreateModel(
            name='UserBadgeProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('progress_value', models.BigIntegerField(default=0)),
                ('progress_target', models.BigIntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulse.users')),
            ],
            options={
                'db_table': 'UserBadgeProgress',
            },
        ),
        migrations.AddConstraint(
            model_name='badge',
            constraint=models.CheckConstraint(condition=models.Q(('associated_tag__isnull', True), ('is_global', False), _connector='OR'), name='mutual_exclusivity_check'),
        ),
        migrations.AlterUniqueTogether(
            name='badgetier',
            unique_together={('badge', 'tier_level')},
        ),
        migrations.AlterUniqueTogether(
            name='userbadge',
            unique_together={('user', 'badge')},
        ),
        migrations.AlterUniqueTogether(
            name='userbadgeprogress',
            unique_together={('user', 'badge')},
        ),
    ]