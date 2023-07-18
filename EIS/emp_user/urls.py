from django.urls import path
from . import views

urlpatterns = [
    path('emp_home', views.emp_home, name='emp_home'),
]