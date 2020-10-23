from django.db import models
import re
import bcrypt
import datetime
# Create your models here.

class UserManager(models.Manager):
    # Basic Validation and Duplicate Detection
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First Name must be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last Name must be at least 3 characters"
        if len(postData['email']) < 7:
            errors['email'] = "Email must be at least 7 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "Email must be in the correct format ex: email@provider.com"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters "
        if not postData['password_confirm'] == postData['password']:
            errors['password_confirm'] = "Password does not match Confirm Password"
        if len(User.objects.filter(email=postData['email'])):
            errors['duplicate'] = "Email already exists"
        if postData['dob'] > str(datetime.date.today()):
            errors['dob'] = "This date is invalid"

        # Create a date object to compare with postData['dob']
        today = datetime.datetime.now()
        requiredAge = 13
        age_requirement_date = "" + str(today.year - requiredAge) + "-" + str(today.month) + '-' + str(today.day)
        if str(postData['dob']) > age_requirement_date:
            errors['too_young'] = "You must be at least " + str(requiredAge) + " years old to use this site"
        
        return errors

    def login_validator(self, postData):
        # Validates Login Info
        login_errors = {}

        if postData['login_email']:
            thisUser = User.objects.filter(email=postData['login_email']).first()
            if thisUser:
                if not bcrypt.checkpw(postData['login_password'].encode(), thisUser.password.encode()):
                    login_errors['login_password'] = "Invalid Credentials"
            else:
                login_errors['login_email'] = "Email not in our database"
        else:
            login_errors['login_email'] = "Please enter a valid email"

        return login_errors

    def contact_validator(self, postData):
        contact_errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['full_name']) < 4:
            contact_errors['full_name'] = "Name must be at least 4 characters"
        if len(postData['phone_number']) < 10:
            contact_errors['phone_number'] = "Number must be at least 10 characters"
        if len(postData['email']) < 7:
            contact_errors['email'] = "Email must be at least 7 characters"
        if not EMAIL_REGEX.match(postData['email']):
            contact_errors['email_regex'] = "Email must be in the correct format ex: email@provider.com"

        return contact_errors
    
    def appointment_validator(self, postData):
        appointment_errors = {}
        if len(User.objects.filter(address=postData['address'])):
            errors['duplicate_address'] = "Appointment already exists."
        if postData['date'] > str(datetime.date.today()):
            errors['date'] = "This date is invalid"

        return appointment_errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    usertype = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Car(models.Model):
    make= models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    year = models.IntegerField()
    user = models.ForeignKey(User, related_name="cars", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="appointments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


