from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class User(models.Model):
  first_name =  models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  email = models.EmailField(max_length=225)
  password = models.CharField(max_length=225)
  confirm_password = models.CharField(max_length=225)  
  dob = models.DateField()
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  mobile = models.CharField(max_length=255)
  gender = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role.name})'

class Patient(models.Model):
  ##
  description = models.TextField
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass

class Therapy(models.Model):
  ##
  available_time = models.DateTimeField()
  experience = models.TextField()
  location = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass

class Assessment(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  mental_wellness = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass

class Question(models.Model):
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass

class Response(models.Model):## ManyToMany or forginkey
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer = models.TextField()
  score = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass

class Appointment(models.Mode):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    pass
