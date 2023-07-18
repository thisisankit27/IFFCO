from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from emp_user.models import empUser, salary
from .models import Attendance

@staff_member_required(login_url='login')
def staff_home(request):
    try:
        employee = empUser.objects.get(user = request.user)
    except empUser.DoesNotExist:
        employee = empUser(
        user=request.user,
        dob=datetime.date(1990, 5, 15),
        doj=datetime.date.today(),
        qualification="Bachelor",
        address="123 Main St, City",
        pan="ABCDE1234F",
        aadhar="123456789012",
        emp_status="active",
        bank_account="0123456789",
        basic_salary=5000.00,
        created_by="admin",
        updated_by="admin")
        employee.save()
    try:
        salary_info = salary.objects.get(emp=employee)
        salary_info.total_income = Decimal(
                    Decimal(employee.basic_salary) +
                    (Decimal(employee.basic_salary) * Decimal(salary_info.DA_per) / 100) +
                    (Decimal(employee.basic_salary )* Decimal(salary_info.Allowances_per) / 100)
                )
        salary_info.save()
    except salary.DoesNotExist:
        # Create a new salary object for the employee
        salary_info = salary(emp=employee)
        salary_info.total_income = Decimal(
                    Decimal(employee.basic_salary) +
                    (Decimal(employee.basic_salary) * Decimal(salary_info.DA_per) / 100) +
                    (Decimal(employee.basic_salary )* Decimal(salary_info.Allowances_per) / 100)
                )
        salary_info.save()
    context = {
        'emp_user': employee,
        'dob_string': employee.dob.strftime('%Y-%m-%d'),  # Convert dob to string format
        'doj_string': employee.doj.strftime('%Y-%m-%d'),
        'salary': salary_info,  # Pass the salary object to the context
    }
    return render(request, 'staff_home_components/staff_home.html', context)

@staff_member_required(login_url='login')
def staff_emp_list(request):
    staff_employees = empUser.objects.filter(user__is_staff=True)
    non_staff_employees = empUser.objects.exclude(user__is_staff=True)
    context = {'employees': non_staff_employees,
               'staff_employees': staff_employees}
    return render(request, 'staff_home_components/staff_emp_list.html', context)

@staff_member_required(login_url='login')
def emp_full_detail(request, employee_id):
    employee = empUser.objects.get(id=employee_id)
    try:
        salary_info = salary.objects.get(emp=employee)
    except salary.DoesNotExist:
        # Create a new salary object for the employee
        salary_info = salary(emp=employee)
        salary_info.save()
    context = {
        'emp_user': employee,
        'dob_string': employee.dob.strftime('%Y-%m-%d'),  # Convert dob to string format
        'doj_string': employee.doj.strftime('%Y-%m-%d'),
        'salary': salary_info,  # Pass the salary object to the context
    }
    return render(request, 'staff_home_components/emp_full_detail.html', context)

@staff_member_required(login_url='login')
def edit_employee(request, employee_id):
    employee = empUser.objects.get(id=employee_id)
    user = employee.user  # Get the associated User object
    try:
        salary_info = salary.objects.get(emp=employee)
    except salary.DoesNotExist:
        # Create a new salary object for the employee
        salary_info = salary(emp=employee)
        salary_info.save()


    if request.method == 'POST':
        # Update the employee details based on the form data
        employee.dob = request.POST['dob']
        employee.doj = request.POST['doj']
        employee.qualification = request.POST['qualification']
        employee.address = request.POST['address']
        employee.pan = request.POST['pan']
        employee.aadhar = request.POST['aadhar']
        employee.emp_status = request.POST['emp_status']
        employee.bank_account = request.POST['bank_account']
        employee.basic_salary = request.POST['basic_salary']
        
        # Update details:
        employee.updated_by = request.user.username
        employee.updated_dt = datetime.datetime.now()
        employee.save()
        
        # salary Updation
        da_allowances = request.POST['da_allowances']
        allowances_per = request.POST['da_per']
        
        salary_info.DA_per = da_allowances
        salary_info.Allowances_per = allowances_per
        salary_info.total_income = Decimal(
                    Decimal(employee.basic_salary) +
                    (Decimal(employee.basic_salary) * Decimal(da_allowances) / 100) +
                    (Decimal(employee.basic_salary )* Decimal(allowances_per) / 100)
                )
        salary_info.save()

        # Update the first_name and last_name of the associated User object
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        updated_username = request.POST['username']
        if User.objects.filter(username=updated_username).exists():
            messages.error(request, 'That username is taken')
            return redirect('edit_employee', employee_id=employee_id)
        else:
            user.username = updated_username
            user.save()
        return redirect('staff_emp_list')

    context = {
        'employee': employee,
        'dob_string': employee.dob.strftime('%Y-%m-%d'),  # Convert dob to string format
        'doj_string': employee.doj.strftime('%Y-%m-%d'),
        'salary': salary_info,
    }
    return render(request, 'staff_home_components/edit_employee.html', context)

@staff_member_required(login_url='login')
def staff_emp_attendance(request):
    date_filter = request.GET.get('date')
    username_search = request.GET.get('username')

    attendance_list = Attendance.objects.all()

    # Apply date filter if provided
    if date_filter:
        attendance_list = attendance_list.filter(date=date_filter)

    # Apply username search if provided
    if username_search:
        attendance_list = attendance_list.filter(employee__user__username__icontains=username_search)

    context = {
        'attendance_list': attendance_list
    }

    return render(request, 'staff_home_components/staff_emp_attendance.html', context)

@staff_member_required(login_url='login')
def mark_attendance(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            employee = empUser.objects.get(user__username=username)
            current_date = datetime.date.today()

            # Check if attendance for the employee and current date already exists
            if Attendance.objects.filter(employee=employee, date=current_date).exists():
                messages.error(request, 'Attendance already marked for today')
                return redirect('staff_emp_attendance')

            # Mark attendance for the employee
            attendance = Attendance(
                employee=employee,
                date=current_date,
                shift=request.POST.get('shift', 'A'),  # Set the default shift here
                marked_by=request.user.username
            )
            attendance.save()

            # Update the employee object
            employee.updated_by = request.user.username
            employee.updated_dt = datetime.datetime.now()
            employee.save()

            messages.success(request, 'Attendance marked successfully')
            return redirect('staff_emp_attendance')

        except empUser.DoesNotExist:
            messages.error(request, 'Employee not found')
            return redirect('staff_emp_attendance')
    else:
        return render(request, 'staff_home_components/staff_emp_attendance.html')