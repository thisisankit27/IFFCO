from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.contrib import messages
from datetime import datetime

from decimal import Decimal

from emp_user.models import empUser, salary
from staff_user.models import AttendaceVerification
# Create your views here.

@staff_member_required(login_url='login')
def register(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        dob = request.POST['dob']
        doj = request.POST['doj']
        qualification = request.POST['qualification']
        address = request.POST['address']
        pan = request.POST['pan']
        aadhar = request.POST['aadhar']
        emp_status = request.POST['emp_status']
        bank_account = request.POST['bank_account']
        basic_salary = Decimal(request.POST['basic_salary'])
        da = Decimal(request.POST['da'])
        allowance = Decimal(request.POST['allowance'])

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                user = User(username=username, first_name=first_name, last_name=last_name, is_staff=False)
                user.set_password(password)  # Automatically Store Hashed Password
                user.save()

                emp = empUser(
                    user=user, dob=dob, doj=doj, qualification=qualification, address=address, pan=pan,
                    aadhar=aadhar, emp_status=emp_status, bank_account=bank_account, basic_salary=basic_salary
                )
                emp.save()

                total_income = Decimal(
                    Decimal(basic_salary) +
                    (Decimal(basic_salary) * Decimal(da) / 100) +
                    (Decimal(basic_salary) * Decimal(allowance) / 100)
                )

                salary_info = salary(
                    emp=emp, DA_per=da, Allowances_per=allowance, total_income=total_income
                )
                salary_info.save()

                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    return render(request, 'signup.html')

def get_user_location(address):
    try:
        geolocator = Nominatim(user_agent='iffco_eis_attendance')
        location = geolocator.geocode(address, timeout=10)
        return location
    except GeocoderTimedOut:
        return get_user_location(address)


def is_within_campus(latitude, longitude):
    # Define the latitude and longitude ranges that represent your campus boundaries
    campus_latitude_min = 25.432621164376997
    campus_latitude_max = 25.434140991427014
    campus_longitude_min = 81.8299104964264
    campus_longitude_max = 81.83206281189844

    # Check if the provided latitude and longitude are within the campus boundaries
    if campus_latitude_min <= latitude <= campus_latitude_max and campus_longitude_min <= longitude <= campus_longitude_max:
        return True
    else:
        return False


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
            
#             # Retrieve latitude and longitude from POST data
#             latitude = float(request.POST.get('latitude'))
#             longitude = float(request.POST.get('longitude'))

#             # Perform attendance verification based on location
#             if is_within_campus(latitude, longitude):
#                 # Attendance verified
#                 # Update your Attendance model or perform necessary actions
#                 employee = empUser.objects.get(user=user)
#                 attendance_verification = AttendaceVerification.objects.create(employee=employee,date= datetime.date.today(), attendance_verified=True)
#                 attendance_verification.save()
#                 messages.success(request, 'Attendance verified!')
#             else:
#                 # Attendance not verified
#                 messages.warning(request, 'Attendance not verified.')
#         else:
#             messages.error(request, 'Invalid credentials')

#         return redirect('home')

#     return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')