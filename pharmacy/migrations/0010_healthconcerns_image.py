# Generated by Django 4.2.8 on 2024-01-20 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0009_productbrand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthconcerns',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='health_concerns/'),
        ),
    ]
