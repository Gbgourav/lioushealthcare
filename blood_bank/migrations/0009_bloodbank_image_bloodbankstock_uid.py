# Generated by Django 4.2.8 on 2024-01-28 19:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank', '0008_alter_bloodbankstock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodbank',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blood_bank/'),
        ),
        migrations.AddField(
            model_name='bloodbankstock',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
