from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        return redirect('staff_home')  # Redirect to the admin home page
    else:
        return redirect('emp_home')  # Redirect to the regular user home page
