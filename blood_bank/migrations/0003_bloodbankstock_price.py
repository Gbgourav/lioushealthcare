# Generated by Django 4.2.8 on 2024-01-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank', '0002_bloodbank_bloodgroup_bloodbankstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodbankstock',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
