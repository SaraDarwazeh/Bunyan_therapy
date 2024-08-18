from django.db import models
import re
import bcrypt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

# class Manger to register and login user
class UserManger(models.Manager):
    #validations for user
    def register(self,postData):
        errors ={}
        # validation First Name ## change how may chracter for all and msg
        if len(postData['first_name'])<2:
            errors['first_name'] = 'First Name Should be at least 2 character'
        # validation Last Name ## change how may chracter for all and msg appears
        if len(postData['last_name'])<2:
            errors['last_name'] = 'Last Name Should be at least 2 character'
        # validation username and exists
        if len(postData['username'])<2:
            errors['username'] = 'Username Should be at least 2 character!'
        if  User.objects.filter(username=postData['username']).exists():
            errors['username_user'] = 'Email already in use!'
        # validation Email to regiex for gmail only and exists
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = 'Invalid email address!'
        if  User.objects.filter(email=postData['email']).exists():
            errors['email_used'] = 'Email already in use!'
        # validation Password and confirm are matches and len
        if len(postData['password'])<2:
            errors['password'] = 'First Name Should be at least 2 character'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords are not match'
        # Validate gender
        if 'gender' not in postData or postData['gender'] not in ['male', 'female']:
            errors['gender'] = 'Gender must be selected'    
        # validated dob to required in database and age grater than 13
        if not postData['dob']:
            errors['dob'] = 'Date of Birth is required'
        else:
                dob = datetime.strptime(postData['dob'], '%Y-%m-%d').date()
                today = datetime.now().date()
                age = today.year - dob.year
                if dob >= today:
                    errors['dob_past'] = 'Date of Birth must be in the past'
                elif age < 13:
                    errors['dob'] = 'Age must be at least 13 years'      
        # validation mobile number i think use regex ## if didn't use remove
        if len(postData['mobile'])<14:
            errors['mobile'] = 'Mobile Should be at least 2 character'
        pattern = re.compile(r'^\+?\d{1,4}[\s-]?\d{7,15}$')
        if not pattern.match(postData['mobile']):
            errors['mobile_pattern'] = 'Invalid mobile number format'
        #Explanation of the Regex Pattern: 0097 599936337
        # ^\+?\d{1,4}: Matches an optional + followed by 1 to 4 digits for the country code.
        # \s?: Allows an optional space after the country code.
        # \d{7,15}$: Matches 7 to 15 digits for the rest of the phone number.
        return errors
    # Authorize email and password
    def login(self,postData):
        errors = {}
        try:  
            user = User.objects.get(email=postData['email'])
        except ObjectDoesNotExist:
            errors['email'] = "Email not found."
            return errors
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['password'] = "Invalid password."
        return errors

class User(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)#
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    dob = models.DateField()
    mobile = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='profile_pics/', null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Patient(User):
    medical_history = models.TextField()

    def __str__(self):
        return f'Patient: {self.first_name} {self.last_name}'

class Therapist(User):
    available_time = models.DateTimeField()
    experience = models.TextField()
    location = models.TextField()
    
    def __str__(self):
        return f'Therapist: {self.first_name} {self.last_name}, Location: {self.location}'

class Question(models.Model):#Add from admin panel
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Choice(models.Model):#Add from admin panel
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    points = models.IntegerField()  # Points from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return f'{self.text} ({self.points} points)'

class Response(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True,blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Response to {self.question}: {self.selected_choice.text}'

class Assessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    mental_wellness = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Assessment for {self.patient}'

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Appointment with {self.therapist} for {self.patient}'

class Specialization(models.Model): #Add from admin panel
    title = models.CharField(max_length=45)
    description = models.TextField()
    therapists = models.ManyToManyField(Therapist, related_name='specializations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

#All Patients
def all_patients():
    return Patient.objects.all()
#All therapists
def all_therapist():
    return Therapist.objects.all()
# patient ID
def patient(patient_id):
    return Patient.objects.get(id=patient_id)
#therapist ID
def therapist(therapist_id):
    return Therapist.objects.get(id=therapist_id)
#Create User 
def create_patient(POST):
    password = POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return Patient.objects.create(
        first_name = POST['first_name'],
        last_name = POST['last_name'],
        username = POST['username'],
        email = POST['email'],
        password = hashed_password,
        dob = POST['dob'],
        mobile = POST['mobile'],
        gender = POST['gender'],
        medical_history = POST['medical_history'],
    )
#update information of patient,Can we make change pass and use to forget password
def update_patient(POST,patient_id):
    patient=patient(patient_id)
    patient.first_name = POST['first_name']
    patient.last_name = POST['last_name']
    patient.username = POST['username']
    patient.email = POST['email']
    patient.dob = POST['dob']
    patient.mobile = POST['mobile']
    patient.save()
# deactivate of patient account
def deactivate_user(POST):
    patient = patient(POST['patient_id'])
    patient.delete()
# response patient
def response_patient():
    pass
# add appointment and updated the appointment and deleted
def appointment(appointment_id):
    return Appointment.objects.get(id=appointment_id)
def create_appointment():
    pass
def update_appointment():
    pass
def remove_appointment(POST):
    appointment=appointment(id=POST['appointment_id'])
    appointment.delete()
    
#QUERY NEED

# show all appointments 
# for patients side all appointments
# and the doctors side all appointments

# all data for Response and assessments
# add function for specializations appear with therapist
# search how to calculate the score of mental wellness
#  validation for appointment and response