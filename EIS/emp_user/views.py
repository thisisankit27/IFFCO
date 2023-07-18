from django.shortcuts import render

# Create your views here.

def emp_home(request):
    return render(request, 'emp_home.html')