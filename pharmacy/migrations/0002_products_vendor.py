# Generated by Django 4.2.8 on 2024-01-17 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0022_bookdoctorslot_service_type'),
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vendor.pharmacyvendor'),
            preserve_default=False,
        ),
    ]
