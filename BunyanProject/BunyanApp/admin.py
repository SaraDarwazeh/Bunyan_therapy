from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Patient)
admin.site.register(Therapist)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(Assessment)
admin.site.register(Specialization)
admin.site.register(Appointment)