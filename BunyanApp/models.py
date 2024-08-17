from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    confirm_password = models.CharField(max_length=225)  
    dob = models.DateField()
    mobile = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role.name})'

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

class Assessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    mental_wellness = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Assessment for {self.patient}'

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Response to {self.question}'

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
