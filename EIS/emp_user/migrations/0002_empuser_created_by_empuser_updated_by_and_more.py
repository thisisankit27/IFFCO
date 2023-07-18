# Generated by Django 4.2.3 on 2023-07-06 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empuser',
            name='created_by',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AddField(
            model_name='empuser',
            name='updated_by',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AddField(
            model_name='empuser',
            name='updated_dt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]