from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):

  return render(request,'index.html')

def assessment(request):
  context = {
    'questions':all_questions(),
    'choices':all_choices(),
  }
  return render(request,'assessment.html',context)

def login(request):
  return render(request,'login.html')

def register(request):
  if request.method == 'POST':
    errors = User.objects.register(request.POST)

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/login')
    else:
      create_patient(request.POST)
      return redirect('/login')

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
                return redirect('/login')
        else:
            messages.error(request, "Invalid password.")
            return redirect('/login')
        return redirect('/')

    


def about(request):
  return render(request,'about.html')

def team(request):
  return render(request,'team.html')

def contact(request):
  return render(request,'contact.html')

def services(request):
  return render(request,'services.html')
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