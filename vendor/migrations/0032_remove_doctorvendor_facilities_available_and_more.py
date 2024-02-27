# Generated by Django 4.2.8 on 2024-02-19 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0031_facilities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorvendor',
            name='facilities_available',
        ),
        migrations.RemoveField(
            model_name='doctorvendor',
            name='fees',
        ),
        migrations.RemoveField(
            model_name='doctorvendor',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='doctorvendor',
            name='sub_specialty',
        ),
        migrations.AddField(
            model_name='bloodbankvendor',
            name='facilities',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.facilities'),
        ),
        migrations.AddField(
            model_name='doctorvendor',
            name='facilities',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.facilities'),
        ),
        migrations.AddField(
            model_name='pathologyvendor',
            name='facilities',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.facilities'),
        ),
        migrations.AddField(
            model_name='pharmacyvendor',
            name='facilities',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.facilities'),
        ),
        migrations.AddField(
            model_name='phlebologistvendor',
            name='facilities',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.facilities'),
        ),
    ]