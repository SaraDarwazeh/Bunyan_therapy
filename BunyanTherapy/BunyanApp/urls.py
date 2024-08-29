from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'BunyanApp'
urlpatterns = [
    path('Home/', views.index, name='Home'),
    path('login/', views.login,name='login'),
    path('register/',views.register),
    path('sign_up/',views.sign_up),
    path('assessment/', views.assessment,name='assessment'),
    path('about/', views.about,name='about'),
    path('team/', views.team,name='team'),
    path('contact/', views.contact,name='contact'),
    path('services/', views.services,name='services'),
    path('team/<str:first_name>-<str:last_name>/profile',views.therapist_info),
    path('logout/', views.logout,name='logout'),
    # path('calculate_assessment_points/', views.calculate_assessment_points, name='calculate_assessment_points'),
    # path('assessment_result/<int:assessment_id>/', views.assessment_result, name='assessment_result'),
    path('profile/<int:patient_id>', views.profile,name='profile'),
    path('update_profile_patient/<int:patient_id>',views.edit_profile,name='edit_profile'),
    path('choose_assessment/', views.choose_assessment, name='choose_assessment'),
    path('take_assessment/<int:assessment_id>/', views.take_assessment, name='take_assessment'),
    path('booking/<str:first_name>-<str:last_name>', views.booking,name='Booking'),
    path('assessment_result/<int:assessment_id>/', views.assessment_result, name='assessment_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)