# Generated by Django 4.2.8 on 2024-01-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0008_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='brand/'),
        ),
    ]