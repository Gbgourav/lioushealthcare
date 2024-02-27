# Generated by Django 4.2.8 on 2024-01-30 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labtests', '0007_labtest_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('delivered_data', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_for_test', to='payment.payment')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_product', to='labtests.labcart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
