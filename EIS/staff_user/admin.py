from django.contrib import admin

from .models import Attendance, AttendaceVerification

# Register your models here.

admin.site.register(Attendance)
admin.site.register(AttendaceVerification)