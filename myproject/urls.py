"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user_auth import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path('blog/', views.blog_list, name='blog_list'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('DoctorDetails/', views.DoctorDetails, name='DoctorDetails'),
    path('all_blogs/', views.all_blogs, name='all_blogs'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('appointments/book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('appointments/confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
