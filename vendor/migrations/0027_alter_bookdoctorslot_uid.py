# Generated by Django 4.2.8 on 2024-01-30 18:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0026_alter_bookdoctorslot_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdoctorslot',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]