from django.db import models
import bcrypt
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django_countries.fields import CountryField
import pycountry
import re

# class Manager to register and login user
class UserManager(models.Manager):
    def register(self, postData):
        errors = {}
        # Validate registration inputs
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
 #       if not EMAIL_REGEX.match(postData['email']):
 #           errors['email'] = "Invalid email format."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match."

        if not errors:
            # Hash the password and save the new user
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
            self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed_pw
            )

        return errors




    def login(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
        except User.DoesNotExist:
            errors['email'] = "Email not found."
            return errors

        # Ensure the stored password is a valid bcrypt hash
        if not user.password.startswith('$2b$') or len(user.password) != 60:
            errors['password'] = "Invalid password format."
        else:
            # Check if the password matches
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."

        return errors

class Language(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    code = models.CharField(max_length=10, null=True, blank=True, default='')
    
    def __str__(self):
        return self.name

class User(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True, default='')
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=255, null=True, blank=True, default='')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def get_age(self):
        if not self.dob:
            return "Unknown"
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Patient(User):
    medical_history = models.TextField(default='')

    def __str__(self):
        return f'Patient: {self.first_name} {self.last_name}'

class Specialization(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Therapist(User):
    available_time = models.DateTimeField()
    experience_years = models.IntegerField(blank=True, default=0)
    location = models.TextField(default='')
    specializations = models.ManyToManyField(Specialization, blank=True, related_name='therapists')
    
    def __str__(self):
        return f'Therapist: {self.first_name} {self.last_name}, Location: {self.location}'

# class Question(models.Model):
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.text

# class Choice(models.Model):
#     question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     points = models.IntegerField()  # Points from 1 to 5
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f'{self.text} ({self.points} points)'

# class Response(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f'Response to {self.question}: {self.selected_choice.text}'

class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('emotional_wellbeing', 'Emotional Well-being'),
        ('cognitive_functioning', 'Cognitive Functioning'),
        ('lifestyle_habits', 'Lifestyle and Habits'),
    ]

    type = models.CharField(max_length=50, choices=ASSESSMENT_TYPES, default='emotional_wellbeing')

    def __str__(self):
        return self.get_type_display()



class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255,default='default_value')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    points = models.IntegerField()  # Points from 0 to 4

    def __str__(self):
        return f"{self.text} ({self.points} points)"

class UserAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Default score to 0
    result = models.CharField(max_length=255, default='Not assessed')  # Default result
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Appointment with {self.therapist} for {self.patient}'

# Utility Functions

# All Patients
def all_patients():
    return Patient.objects.all()

# All Therapists
def all_therapists():
    return Therapist.objects.all()

# Patient by ID
def patient(patient_id):
    return Patient.objects.get(id=patient_id)

# Therapist by ID
def therapist(therapist_id):
    return Therapist.objects.get(id=therapist_id)

# User by Email
def user_email(POST):
    return User.objects.filter(email=POST['email']) 

# Create Patient
def create_patient(POST):
    password = POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return Patient.objects.create(
        first_name=POST['first_name'],
        last_name=POST['last_name'],
        email=POST['email'],
        password=hashed_password,
    )

# Update Patient Information
def update_patient(POST, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.first_name = POST['first_name']
    patient.last_name = POST['last_name']
    patient.username = POST['username']
    patient.email = POST['email']
    patient.dob = POST['dob']
    patient.mobile = POST['mobile']
    patient.save()

# Deactivate Patient Account
def deactivate_user(POST):
    patient = Patient.objects.get(id=POST['id'])
    patient.active = False
    patient.save()


