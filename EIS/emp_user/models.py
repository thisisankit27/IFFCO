from django.db import models
from decimal import Decimal

from django.contrib.auth.models import User

class empUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField()
    doj = models.DateField()
    qualification = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=10)
    aadhar = models.CharField(max_length=12)
    emp_status = models.CharField(max_length=10, choices=(('active', 'Active'), ('retired', 'Retired')))
    bank_account = models.CharField(max_length=255)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=255, default='admin')
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255 , default='admin')
    updated_dt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

class salary(models.Model):
    emp = models.ForeignKey(empUser, on_delete=models.CASCADE)
    DA_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    Allowances_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_income = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

    def __str__(self):
        return self.emp.user.username
