# Generated by Django 4.2.8 on 2024-02-25 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0044_doctorvendor_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdoctorslot',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
