# Generated by Django 4.2.8 on 2024-01-17 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_products_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthConcerns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='health_concerns',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.healthconcerns'),
        ),
    ]