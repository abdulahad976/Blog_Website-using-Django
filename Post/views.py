from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                send_mail(
                    "Login Alert",
                    "You have just logged into your account.",
                    "Business Purpose Email",
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send email to {user.email}: {e}")

            return redirect('dashboard')
        else:
            logger.debug(f"Form errors: {form.errors}")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})





# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             send_mail(
#                 "Login Alert",
#                 "You have just Logged into Your Account ",
#                 "Business Purpose",
#                 [user.email],
#                 fail_silently=False,
#             )
#             return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()

            send_mail(
                "Account Created ",
                "You have just Created Your Account ",
                "Business Purpose",
                [user.email],
                fail_silently=False,
            )
            return redirect('login')  # Replace 'home' with your desired redirect URL
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})





def dashboard_view(request):
    users = User.objects.all()
    print(users)
    if request.user.is_authenticated:
        username = f"{request.user.first_name} {request.user.last_name}".strip()
        print(username)
    else:
        username = ''

    return render(request, 'dashboard.html', {'username': username})


def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'home' with your desired redirect URL after logout


def home(request):
    # post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'home.html')

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')
