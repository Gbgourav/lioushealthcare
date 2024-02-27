# Generated by Django 4.2.8 on 2024-01-10 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_object_id', models.PositiveIntegerField()),
                ('time', models.TimeField()),
                ('day', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=3)),
                ('vendor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
