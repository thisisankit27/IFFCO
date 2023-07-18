# Generated by Django 4.2.3 on 2023-07-05 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='empUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('doj', models.DateField()),
                ('qualification', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('pan', models.CharField(max_length=10)),
                ('aadhar', models.CharField(max_length=12)),
                ('emp_status', models.CharField(choices=[('active', 'Active'), ('retired', 'Retired')], max_length=10)),
                ('bank_account', models.CharField(max_length=255)),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]