# Generated by Django 4.2.8 on 2024-02-05 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('accounts', '0006_states'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country')),
            ],
        ),
    ]
