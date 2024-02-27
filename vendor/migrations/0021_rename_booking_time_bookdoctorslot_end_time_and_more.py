# Generated by Django 4.2.8 on 2024-01-16 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0020_rename_time_slottime_end_time_slottime_start_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookdoctorslot',
            old_name='booking_time',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='bookdoctorslot',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctorvendor',
            name='clinic_visit_fees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctorvendor',
            name='video_consultation_fees',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]