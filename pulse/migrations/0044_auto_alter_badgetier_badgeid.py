from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('pulse', '0043_alter_badge_badge_id_alter_badgetier_id_and_more'),  # Replace with the actual last migration
    ]

    operations = [
        migrations.AlterField(
            model_name='badgetier',
            name='badge',
            field=models.ForeignKey(
                to='pulse.badge',
                on_delete=models.CASCADE,
                related_name='tiers',
                db_column='badge_id',
            ),
        ),
        migrations.AlterField(
            model_name='badgetier',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
