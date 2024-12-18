# Generated by Django 4.2.8 on 2024-01-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0017_phlebologistvendor_timing_timing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='doctorvendor',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.service'),
        ),
        migrations.AddField(
            model_name='pathologyvendor',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.service'),
        ),
        migrations.AddField(
            model_name='pharmacyvendor',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.service'),
        ),
        migrations.AddField(
            model_name='phlebologistvendor',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.service'),
        ),
    ]
