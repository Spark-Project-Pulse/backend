from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0040_merge_20241202_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='badge_id',
        ),
        migrations.AddField(
            model_name='badge',
            name='badge_id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
