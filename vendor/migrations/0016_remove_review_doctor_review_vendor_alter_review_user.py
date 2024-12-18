# Generated by Django 4.2.8 on 2024-01-11 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendor', '0015_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='doctor',
        ),
        migrations.AddField(
            model_name='review',
            name='vendor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='vendor_reviews', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
