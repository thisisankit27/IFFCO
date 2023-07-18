from django.urls import path
from . import views

urlpatterns = [
    path('staff_home', views.staff_home, name='staff_home'),
    path('staff_emp_list', views.staff_emp_list, name='staff_emp_list'),
    path('edit_employee/<int:employee_id>', views.edit_employee, name='edit_employee'),
    path('emp_full_detail/<int:employee_id>', views.emp_full_detail, name='emp_full_detail'),
    path('staff_emp_attendance', views.staff_emp_attendance, name='staff_emp_attendance'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
]