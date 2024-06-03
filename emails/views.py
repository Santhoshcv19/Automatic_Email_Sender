from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate

def send_welcome_email(user_email):
    subject = 'Welcome to my Site'
    message = 'Thank you for signing up.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = user.username, password = raw_password)
            login(request, user)
            send_welcome_email(user.email)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'emails/signup.html', {'form': form})
    
def home(request):
    return render(request, 'emails/home.html')
# Create your views here.
