# Generated by Django 4.2.3 on 2023-07-06 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='in_punch_time',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='out_punch_time',
        ),
    ]