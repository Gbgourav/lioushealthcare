# Generated by Django 4.2.8 on 2024-01-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0013_remove_productbrand_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]