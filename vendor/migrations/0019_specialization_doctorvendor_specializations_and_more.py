# Generated by Django 4.2.8 on 2024-01-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0018_service_doctorvendor_services_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='doctorvendor',
            name='specializations',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.specialization'),
        ),
        migrations.AddField(
            model_name='pathologyvendor',
            name='specializations',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.specialization'),
        ),
        migrations.AddField(
            model_name='pharmacyvendor',
            name='specializations',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.specialization'),
        ),
        migrations.AddField(
            model_name='phlebologistvendor',
            name='specializations',
            field=models.ManyToManyField(blank=True, null=True, to='vendor.specialization'),
        ),
    ]