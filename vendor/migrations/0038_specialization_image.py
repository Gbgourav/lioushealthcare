# Generated by Django 4.2.8 on 2024-02-21 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0037_alter_pharmacyvendor_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='specialization/'),
        ),
    ]
