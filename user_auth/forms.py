from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import BlogPost,Appointment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'profile_picture', 'address_line1', 'city', 'state', 'pincode','email')



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'is_draft']

#New updated task3 form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['specialty', 'date', 'start_time']
        
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'start_time': forms.TextInput(attrs={'type': 'time'}),
        }