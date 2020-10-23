from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.contrib import messages 
from .models import *
import bcrypt
import datetime 


# Create your views here.
def index(request):
	return render_to_response('index.html')


def about(request):
	return render(request, 'about.html')


def service(request):
	return render(request, 'services.html')


def contact(request):
	return render(request, 'contact.html')

def contact_form(request):
	if request.method =='POST':
		contact_errors = User.objects.contact_validator(request.POST)
		if len(contact_errors) > 0:
			for key, value in contact_errors.items():
				messages.info(request, value)
			return redirect('contact')
		else:
			if request.method =='POST':
				Contact.objects.create(
					full_name=request.POST['full_name'],
					phone_number=request.POST['phone_number'],
					email=request.POST['email'],
					message=request.POST['message'],
					)
			return redirect('/')

def login(request):
	return render(request, 'registration/login.html')

def register(request):
	return render(request, 'registration/register.html')

def register_form(request):
	if request.method =='POST':
		reg_errors = User.objects.registration_validator(request.POST)
		if len(reg_errors) > 0:
			for key, value in reg_errors.items():
				messages.error(request,value)
			return redirect('register')
		else:
			hashedPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
			newUser = User.objects.create(
				first_name=request.POST['first_name'],
				last_name=request.POST['last_name'],
				email=request.POST['email'],
				password =hashedPW,
				date_of_birth=request.POST['dob'],
				usertype=request.POST['usertype']
				)
				
			request.session['cur_user'] = newUser.id
		return redirect('login')

def login_form(request):
	if request.method == 'POST':
		login_errors = User.objects.login_validator(request.POST)
		thisUser = User.objects.filter(email = request.POST["login_email"])
		#validate login
		if len(login_errors) or len(thisUser) <= 0:
			for key, value in login_errors.items():
				messages.info(request, value)
			return redirect('/login/')
		else:
			request.session['cur_user'] = thisUser.first().id	
			return redirect('/')

def logout(request):
	request.session.flush()
	return render(request, 'registration/logout.html')

def dashboard(request):
	# if User.objects.filter(usertype= Mechanic):
	context = {
		"user" : User.objects.get(id = request.session['cur_user']),
	}
	return render(request, 'registration/dashboard.html', context)

def My_car(request):
	context = {
        "all_cars" : Car.objects.filter(user_id = request.session['cur_user'])
    }
	return render(request, 'My_Car.html', context)

def Add_car(request):
	if request.method == 'POST':
		newCar = Car.objects.create(
			make = request.POST['make'],
			model = request.POST['model'],
			year = request.POST['year'],
			user = User.objects.get(id = request.session['cur_user'])
		)
		messages.success(request, 'You added a car to your garage!')
	return redirect ('My_car')
	
def del_car(request):
	# if request.method == 'POST':
	delCar = Car.objects.first()
	delCar.delete()
	messages.error(request, 'You removed a car from your garage!')
	return redirect('My_car')

def appointment(request):
	context = {
        "all_appointments" : Appointment.objects.filter(user_id = request.session['cur_user']),
	}

	return render(request, 'appointment.html', context)

def make_appointment(request):
	if request.method == 'POST':
		appointment = Appointment.objects.create(
			date = request.POST['date'],
			time = request.POST['time'],
			address = request.POST['address'],
			user = User.objects.get(id = request.session['cur_user'])
		)
	messages.success(request, 'You Made an Appointment!')

	return redirect ('appointment')

def cancel_appointment(request):
	delappointment = Appointment.objects.first()
	delappointment.delete()
	messages.error(request, 'You canceled an Appointment!')

	return redirect ('appointment')


