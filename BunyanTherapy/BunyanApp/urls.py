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
    #team is ready 
    path('team/', views.team,name='team'),
    path('contact/', views.contact,name='contact'),
    path('services/', views.services,name='services'),
    path('profile/', views.profile,name='profile')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)