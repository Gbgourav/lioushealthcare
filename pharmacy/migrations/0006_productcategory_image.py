# Generated by Django 4.2.8 on 2024-01-20 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0005_alter_healthconcerns_uid_alter_productbrand_uid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
