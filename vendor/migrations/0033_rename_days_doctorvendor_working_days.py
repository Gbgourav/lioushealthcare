# Generated by Django 4.2.8 on 2024-02-19 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0032_remove_doctorvendor_facilities_available_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorvendor',
            old_name='days',
            new_name='working_days',
        ),
    ]
