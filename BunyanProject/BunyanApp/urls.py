from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'BunyanApp'
urlpatterns = [
    path('Home/', views.index, name='Home'),
    path('login/', views.login,name='login'),
    path('assesment/', views.assesment,name='assesment'),
    path('about/', views.about,name='about'),
    path('team/', views.team,name='team'),
    path('contact/', views.contact,name='contact'),
    path('services/', views.services,name='services')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)