from django.urls import path, include
from . import views
# from django.contrib.auth import PasswordResetView, PasswordResetDoneView

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('contact_form/', views.contact_form, name='contact_form'),
    path('login/', views.login, name='login'),
    path('login_form/', views.login_form, name='login_form'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register_form/', views.register_form, name='register_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('My_car/', views.My_car, name='My_car'),
    path('Add_car/', views.Add_car, name='Add_car'),
    path('del_car/', views.del_car, name='del_car'),
    path('appointment/', views.appointment, name='appointment'),
    path('make_appointment/', views.make_appointment, name='make_appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
]