# Generated by Django 4.2.8 on 2023-12-28 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_profile_completed',
            field=models.BooleanField(default=False),
        ),
    ]
