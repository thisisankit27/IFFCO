from django.db import models

from django.contrib.auth.models import User
from emp_user.models import empUser
# Create your models here.

class Attendance(models.Model):
    employee = models.ForeignKey(empUser, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C')))
    marked_by = models.CharField(max_length=255, default='admin')
    
class AttendaceVerification(models.Model):
    employee = models.ForeignKey(empUser, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_verified = models.BooleanField(default=False)