from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
import bcrypt

# Home page view
def index(request):
    return render(request, 'index.html')

# Assessment page view
def assessment(request):
    context = {
        'questions': all_questions(),
        'choices': all_choices(),
    }
    return render(request, 'assessment.html', context)

# Login page view
def login(request):
    #if request.session.get('user_id'):
      #  return redirect('/team')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Handle registration logic and collect any errors
        errors = User.objects.register(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/register')  # Redirect back to the registration page

        # Assuming create_patient might throw exceptions, it should be handled by higher-level exception handling or logging
        patient = create_patient(request.POST)
        if patient and patient.email and patient.first_name and patient.last_name:
            # Send the welcome email
            send_registration_email(patient.email, patient.first_name, patient.last_name)
            messages.success(request, 'Registration successful! A welcome email has been sent to you.')
            return redirect(f'/profile/{patient.id}')
        else:
            messages.error(request, 'Registration failed. Please try again.')
            return redirect('/register')  # Redirect back to the registration page

def sign_up(request):
  if request.method == 'POST':
    errors = User.objects.login(request.POST)

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/login')
    else:
        user = user_email(request.POST)
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password .encode()):
                request.session['user_id'] = logged_user.id
                return redirect(f'/profile/{logged_user.id}')
        else:
            messages.error(request, "Invalid password.")
            return redirect('/login')
        return redirect('/')

    
def booking(request,first_name, last_name):
  # if request.session == 'user_id':
    context={
          'user' : get_user(request.session),
          'therapist' :therapist(first_name, last_name),
          
    }
    return render(request,'Booking.html',context)
  # else:
  #   return redirect('/team')

# Profile view
def profile(request, patient_id):
    context = {
        'user': get_user(request.session),
        'patient': get_object_or_404(Patient, id=patient_id),
    }
    return render(request, 'profile.html', context)

# Edit profile view
def edit_profile(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        update_patient(request.POST, patient_id)
        send_update_notification_email(patient.email, patient.first_name, patient.last_name)
        messages.success(request, 'Profile updated successfully! A notification email has been sent.')
        return redirect(f'/profile/{patient_id}')

# About page view
def about(request):
    return render(request, 'about.html')

# Team page view
def team(request):
    context = {
        'therapists': all_therapists()
    }
    return render(request, 'team.html', context)

# Contact page view
def contact(request):
    return render(request, 'contact.html')

# Services page view
def services(request):
  return render(request,'services.html')

def edit_profile(request, patient_id):
    if request.method == 'POST':
            # Update patient information
            patient = Patient.objects.get(id=patient_id)
            update_patient(request.POST, patient_id)
            send_update_notification_email(patient.email, patient.first_name, patient.last_name)
            messages.success(request, 'Profile updated successfully! A notification email has been sent.')
            return redirect(f'/profile/{patient_id}')  # Redirect to the updated profile page
# def index(request):
#     if request.method == "POST":
#         errors = User.objects.basic_validator(request.POST)
#         if errors:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/')

#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         date_of_birth = request.POST.get('dateofbirth')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')
#         photo = request.FILES.get('photo')
#         password = generate_random_password()
#         # password = request.POST.get('password')
#         # confirm_password = request.POST.get('confirm_password')


#         # # Check if passwords match
#         # if password != confirm_password:
#         #     messages.error(request, "Passwords do not match.")
#         #     return redirect('/')

#         # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#         # Create User
#         user = User.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             dateofbirth=date_of_birth,
#             phone_number=phone_number,
#             email=email,
#             password=password,
#             photo = photo,
#         )
#         request.session['first_name'] = first_name

#         # Handle role
#         role_title = request.POST.get('role')
#         custom_role = request.POST.get('custom_role')
#         custom_description = request.POST.get('custom_description')

#         if role_title == 'custom' and custom_role:
#             role = Role.objects.create(
#                 title=custom_role,
#                 description=custom_description,
#                 user=user
                
#             )
#         elif role_title == 'member':
#             role = Role.objects.create(
#                 title=role_title,
#                 description='this is a member',
#                 user=user
#             )
#         elif role_title == 'trainer':
#             role = Role.objects.create(
#                 title=role_title,
#                 description='this is a trainer',
#                 user=user
#             )
#         return redirect('/users')

#     content = {
#         'roles': Role.objects.all(),
#         'users': User.objects.all()
#     }
#     return render(request, 'index.html', content)

      

    
    return render(request, 'services.html')


# Therapist information view
def therapist_info(request, first_name, last_name):
    therapist = get_object_or_404(Therapist, first_name=first_name, last_name=last_name)
    language_names = ', '.join([language.name for language in therapist.languages.all()])
    context = {
        'therapist': therapist,
        'language_names': language_names,
    }
    return render(request, 'therapist_info.html', context)

# Choose assessment view
def choose_assessment(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if user_id is not in session

    user = get_object_or_404(User, id=user_id)
    assessments = Assessment.objects.all()

    # Fetch the assessments completed by the user
    completed_assessments = UserAssessment.objects.filter(user=user)

    return render(request, 'choose_assessment.html', {
        'assessments': assessments,
        'completed_assessments': completed_assessments
    })

# Take assessment view
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Fetch user ID from session and retrieve the User instance
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if user_id is not in session

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        total_points = 0

        for question in assessment.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                total_points += choice.points

        # Create a new UserAssessment entry
        UserAssessment.objects.create(
            user=user,
            assessment=assessment,
            score=total_points
        )

        messages.success(request, 'Assessment submitted successfully!')
        return redirect(f"/assessment_result/{assessment_id}")

    return render(request, 'take_assessment.html', {'assessment': assessment})

# Assessment result view
def assessment_result(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if user_id is not in session

    user = get_object_or_404(User, id=user_id)
    user_assessment = UserAssessment.objects.filter(user=user, assessment=assessment).order_by('-created_at').first()

    score_comment = ""
    if user_assessment:
        score = user_assessment.score
        created_at = user_assessment.created_at

        if 10 <= score <= 15:
            score_comment = "Excellent mental wellness. You’re likely managing stress well and have a strong support system."
        elif 16 <= score <= 25:
            score_comment = "Good mental wellness. You might have occasional stress or concerns but are generally coping well."
        elif 26 <= score <= 35:
            score_comment = "Fair mental wellness. You may be experiencing some challenges and could benefit from additional support or strategies for stress management."
        elif 36 <= score <= 45:
            score_comment = "Poor mental wellness. You might be facing significant challenges and should consider seeking professional help or exploring new coping strategies."
        elif 46 <= score <= 50:
            score_comment = "Very poor mental wellness. You are likely experiencing substantial difficulties and should consider seeking immediate professional assistance and support."

    return render(request, 'assessment_result.html', {
        'assessment': assessment,
        'score': score if user_assessment else None,
        'created_at': created_at if user_assessment else None,
        'score_comment': score_comment
    })

# Email functions
def send_registration_email(patient_email, patient_first_name,patient_last_name):
    subject = 'Thank You for Registering!'
    message = render_to_string('email/thank_you_email.html', {
        'user': {
            'first_name': patient_first_name,
            'last_name': patient_last_name
        }
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient_email]
    )
    email.content_subtype = 'html'
    email.send()

def send_update_notification_email(patient_email, patient_first_name, patient_last_name):
    subject = 'Your Information has been Updated'
    message = render_to_string('email/update_notification_email.html', {
        'patient': {
            'first_name': patient_first_name,
            'last_name': patient_last_name
        }
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient_email]
    )
    email.content_subtype = 'html'
    email.send()

def send_contact_us_email(recipient_name, sender_name, sender_email, subject, message_content):
    subject = 'Thank You for Contacting Us'
    message = render_to_string('email/contact_us.html', {
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'sender_email': sender_email,
        'subject': subject,
        'message_content': message_content
    })
    email_message = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [sender_email]
    )
    email_message.content_subtype = 'html'
    email_message.send()

# Logout view
def custom_logout(request):
    logout(request)
    return redirect('/login')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AppointmentConfiguration
import json

def appointment_config_view(request):
    if request.method == 'POST':
        # Extracting form data from POST request
        min_date = request.POST.get('min_date')
        max_date = request.POST.get('max_date')
        min_time = request.POST.get('min_time')
        max_time = request.POST.get('max_time')
        disabled_days = request.POST.getlist('disabled_days')
        disabled_times = json.loads(request.POST.get('disabled_times', '[]'))
        
        # Update or create the configuration
        config, created = AppointmentConfiguration.objects.update_or_create(
            id=1,  # Assuming there's only one config object
            defaults={
                'min_date': min_date,
                'max_date': max_date,
                'min_time': min_time,
                'max_time': max_time,
                'disabled_days': disabled_days,
                'disabled_times': disabled_times,
            }
        )
        
        return redirect('appointment_config')  # Redirect to the same page to show updated data
    
    # Retrieve the existing configuration
    config = AppointmentConfiguration.objects.first() or AppointmentConfiguration()

    return render(request, 'appointment_config.html', {'config': config})
