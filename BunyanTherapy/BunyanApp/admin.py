from django.contrib import admin
from .models import User, Language, Question, Patient, Therapist, Choice, Assessment, Specialization, Appointment, UserAssessment



# Define a custom admin interface for Therapist
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'available_time', 'experience_years', 'location','email')
    filter_horizontal = ('specializations','languages')  # Provides a multi-select box for specializations

# Define a custom admin interface for Specialization
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

# Register the models with their respective admin interfaces

admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Language)
admin.site.register(Question)
admin.site.register(Patient)
admin.site.register(Choice)
admin.site.register(UserAssessment)
admin.site.register(Assessment)
admin.site.register(Appointment)