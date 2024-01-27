from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, BlogPostForm, AppointmentForm
from .models import CustomUser, BlogPost, Appointment
from itertools import groupby
from .models import BlogCategory
from .google_calendars import create_calendar_event


#view for signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


#view for login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#view for dashboard eighter patient or doctor
@login_required
def dashboard(request):
    user = request.user
    blog_posts = BlogPost.objects.filter(author=user)
    return render(request, 'mainDashboard.html', {'user': user, 'blog_posts': blog_posts})


#view for doctor details
@login_required
def DoctorDetails(request):
    user = request.user
    profile_picture_url = None
    if user.is_authenticated:
        if user.profile_picture:
            profile_picture_url = user.profile_picture.url
        return render(request, 'dashboard.html', {'user': user, 'profile_picture_url': profile_picture_url})
    else:
        return render(request, 'error.html', {'error_message': 'User not authenticated'})


#view for bloglists
@login_required
def blog_list(request):
    blog_posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'doctor_blogs.html', {'blog_posts': blog_posts})


#view for all blogs
def all_blogs(request):
    # Get all blogs (including drafts) by doctors
    blog_posts = BlogPost.objects.filter(author__user_type='doctor').order_by('category')
    # Organize blog posts by category
    organized_blog_posts = {category: list(posts) for category, posts in groupby(blog_posts, key=lambda x: x.category)}

    return render(request, 'all_blogs.html', {'organized_blog_posts': organized_blog_posts})



#view for creating blost post
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            if isinstance(request.user, CustomUser):
                blog_post.author = request.user
                blog_post.save()
                return redirect('dashboard')
            else:
                return render(request, 'error.html', {'error_message': 'Invalid user type'})
    else:
        form = BlogPostForm()
    return render(request, 'create_blog_post.html', {'form': form, 'categories': BlogCategory.objects.all()})


#view for home
def home(request):
    return render(request, 'main.html')


#view for logout
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


#view for bookingappoitment
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, user_type='doctor')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()

            # Call the function to create a calendar event
            create_calendar_event(
                doctor_email=doctor.email,
                patient_name=request.user.get_full_name(),
                appointment_date=str(appointment.date),
                start_time=str(appointment.start_time),
                end_time=str(appointment.end_time),
                specialty=form.cleaned_data['specialty']  # Access 'specialty' field from form
            )

            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})



#view for appointment conformation
@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})

#view for all patients appoitments
@login_required
def patient_appointments(request):
    user = request.user
    appointments = Appointment.objects.filter(patient=user)
    return render(request, 'patient_appointments.html', {'appointments': appointments})



#view for all doctors list
def doctors_list(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'doctors_list.html', {'doctors': doctors})


#view for patient appoitmnets to visible Doctors
@login_required
def patient_appointments(request):
    if request.user.user_type == 'doctor':  # Check if the user is a doctor
        doctor_id = request.user.id  # Get the ID of the logged-in doctor
        appointments = Appointment.objects.filter(doctor_id=doctor_id)  # Filter appointments by doctor ID
    else:
        appointments = Appointment.objects.filter(patient=request.user)  # Filter appointments by patient
    return render(request, 'patient_appointments.html', {'appointments': appointments})
