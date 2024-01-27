from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta,date,time

#new updated task3 models
class CustomUser(AbstractUser):
    user_types = [('patient', 'Patient'), ('doctor', 'Doctor')]
    user_type = models.CharField(max_length=10, choices=user_types)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    google_calendar_token = models.CharField(max_length=255, blank=True, null=True)
    google_calendar_refresh_token = models.CharField(max_length=255, blank=True, null=True)

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None

    def __str__(self):
        return self.username





# Models for creating blogs

class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category_types = [('Mental Health', 'Mental Health'), ('Heart Disease', 'Heart Disease'),('Covid19','Covid19'),('Immunization','Immunization')]
    category = models.CharField(max_length=100,choices=category_types)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Assuming CustomUser is the doctor model
    created_at = models.DateTimeField(auto_now_add=True)

    def truncated_summary(self):
        return ' '.join(self.summary.split()[:15]) + ('...' if len(self.summary.split()) > 15 else '')

    def __str__(self):
        return self.title



#models for appointment

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    specialty = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField(null=False)
    
    #it calculate and set the end time when saving the appointment
    def save(self, *args, **kwargs):
        
        self.end_time = (datetime.combine(date.today(), self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} - {self.date}"