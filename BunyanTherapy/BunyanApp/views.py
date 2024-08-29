from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import bcrypt

def profile(request, patient_id):
    context = {
        'user': get_user(request.session),
        'patient': patient(patient_id),
    }
    return render(request, 'profile.html', context)

def index(request):
    return render(request, 'index.html')

def assessment(request):
    context = {
        'questions': all_questions(),
        'choices': all_choices(),
    }
    return render(request, 'assessment.html', context)

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/register')
        
        try:
            patient = create_patient(request.POST)
            if patient and patient.email and patient.first_name and patient.last_name:
                send_registration_email(patient.email, patient.first_name, patient.last_name)
                messages.success(request, 'Registration successful! A welcome email has been sent to you.')
                return redirect(f'/profile/{patient.id}')
            else:
                messages.error(request, 'Registration failed. Please try again.')
                return redirect('/register')
        except Exception as e:
            messages.error(request, f'Registration failed due to an error: {str(e)}')
            return redirect('/register')

def sign_up(request):
    if request.method == 'POST':
        errors = User.objects.login(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/login')

        user = user_email(request.POST)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect(f'/profile/{logged_user.id}')
        else:
            messages.error(request, "Invalid password.")
        return redirect('/login')
    
    return redirect('/')

def booking(request, first_name, last_name):
    context = {
        'user': get_user(request.session),
        'therapist': therapist(first_name, last_name),
    }
    return render(request, 'Booking.html', context)

def about(request):
    return render(request, 'about.html')

def team(request):
    context = {
        'therapists': all_therapists()
    }
    return render(request, 'team.html', context)

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def edit_profile(request, patient_id):
    if request.method == 'POST':
        patient = Patient.objects.get(id=patient_id)
        update_patient(request.POST, patient_id)
        send_update_notification_email(patient.email, patient.first_name, patient.last_name)
        messages.success(request, 'Profile updated successfully! A notification email has been sent.')
        return redirect(f'/profile/{patient_id}')

def therapist_info(request, first_name, last_name):
    therapist = get_object_or_404(Therapist, first_name=first_name, last_name=last_name)
    language_names = ', '.join([language.name for language in therapist.languages.all()])
    context = {
        'therapist': therapist,
        'language_names': language_names,
    }
    return render(request, 'therapist_info.html', context)

def send_registration_email(user_email, user_first_name, user_last_name):
    subject = 'Thank You for Registering!'
    message = render_to_string('email/thank_you_email.html', {
        'patient': {
            'first_name': user_first_name,
            'last_name': user_last_name
        }
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
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

def logout(request):
    request.session.flush()
    return redirect('/login')

def choose_assessment(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    assessments = Assessment.objects.all()
    completed_assessments = UserAssessment.objects.filter(user=user).order_by('-created_at')

    return render(request, 'choose_assessment.html', {
        'assessments': assessments,
        'completed_assessments': completed_assessments
    })

from django.http import JsonResponse

def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        total_points = 0

        for question in assessment.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                total_points += choice.points

        UserAssessment.objects.create(
            user=user,
            assessment=assessment,
            score=total_points
        )

        # Return a JSON response with the redirect URL
        return JsonResponse({'redirect_url': f"/assessment_result/{assessment_id}"})

    return render(request, 'take_assessment.html', {'assessment': assessment})

def assessment_result(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    user_assessment = UserAssessment.objects.filter(user=user, assessment=assessment).order_by('-created_at').first()

    score_comment = ""
    if user_assessment:
        score = user_assessment.score
        created_at = user_assessment.created_at

        if assessment.type == "cognitive_functioning":
            print(f"HAHAHHAHAHAHAHHAHAHHAAHAHA")
            if 10 <= score <= 15:
                    score_comment = "Excellent cognitive functioning. You’re likely able to concentrate, remember information, and solve problems effectively."
            elif 16 <= score <= 25:
                    score_comment = "Good cognitive functioning. You may experience occasional difficulties but generally manage cognitive tasks well."
            elif 26 <= score <= 35:
                    score_comment = "Fair cognitive functioning. You might face some cognitive challenges and could benefit from strategies to enhance memory and concentration."
            elif 36 <= score <= 45:
                    score_comment = "Poor cognitive functioning. You may be struggling with cognitive tasks and should consider seeking professional evaluation and support."
            elif 46 <= score <= 50:
                    score_comment = "Very poor cognitive functioning. You are likely experiencing significant cognitive difficulties and should seek immediate professional assistance."
            
        elif assessment.type == "emotional_wellbeing":
            if 10 <= score <= 15:
                score_comment = "Excellent mental wellness. You’re likely managing stress well and have a strong support system."
            elif 16 <= score <= 25:
                score_comment = "Good mental wellness. You might have occasional stress or concerns but are generally coping well"
            elif 26 <= score <= 35:
                score_comment = "Fair mental wellness. You may be experiencing some challenges and could benefit from additional support or strategies for stress management"
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
