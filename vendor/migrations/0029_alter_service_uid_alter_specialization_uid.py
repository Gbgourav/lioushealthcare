# Generated by Django 4.2.8 on 2024-02-05 17:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0028_service_uid_specialization_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]