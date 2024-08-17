from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    dob = models.DateField()
    mobile = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    points = models.IntegerField()  # Points from 1 to 5
    
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mental_wellness = models.IntegerField() 
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

class Specialization(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    therapists = models.ManyToManyField(Therapist, related_name="specializations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
