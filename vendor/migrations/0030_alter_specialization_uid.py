# Generated by Django 4.2.8 on 2024-02-05 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0029_alter_service_uid_alter_specialization_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
