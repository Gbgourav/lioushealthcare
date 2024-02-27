# Generated by Django 4.2.8 on 2024-01-28 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_bank', '0006_remove_bloodbankstock_group_bloodbankstock_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbankstock',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
    ]