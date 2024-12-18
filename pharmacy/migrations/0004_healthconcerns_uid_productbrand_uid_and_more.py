# Generated by Django 4.2.8 on 2024-01-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_healthconcerns_products_health_concerns'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthconcerns',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productbrand',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productoffer',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productrating',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productsubcategory',
            name='uid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
