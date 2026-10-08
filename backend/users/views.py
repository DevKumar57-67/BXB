"""

from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')

    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('home')

    """

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import User

from .forms import RegistrationForm
from .utils import send_otp_email
from django.shortcuts import render, redirect
from django.http import HttpResponse


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            request.session['registration_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
            }

            send_otp_email(form.cleaned_data['email'])

            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )

def verify_otp(request):

    registration_data = request.session.get(
        'registration_data'
    )

    if not registration_data:
        return redirect('register')

    if request.method == 'POST':

        otp = request.POST.get('otp', '').strip()

        from .models import EmailOTP

        otp_record = (
            EmailOTP.objects
            .filter(
                email=registration_data['email'],
                verified=False
            )
            .order_by('-created_at')
            .first()
        )

        if not otp_record:
            return render(
                request,
                'users/verify_otp.html',
                {
                    'error': 'OTP not found. Please request a new OTP.'
                }
            )

        if otp_record.expires_at < timezone.now():
            return render(
                request,
                'users/verify_otp.html',
                {
                    'error': 'OTP has expired. Please request a new OTP.'
                }
            )

        if otp_record.attempts >= 5:
            return render(
                request,
                'users/verify_otp.html',
                {
                    'error': 'Too many attempts. Please request a new OTP.'
                }
            )

        if otp != otp_record.otp:

            otp_record.attempts += 1
            otp_record.save()

            return render(
                request,
                'users/verify_otp.html',
                {
                    'error': 'Invalid OTP. Please try again.'
                }
            )

        otp_record.verified = True
        otp_record.save()

        user = User.objects.create_user(
            username=registration_data['username'],
            email=registration_data['email'],
            password=registration_data['password'],
        )

        request.session.pop(
            'registration_data',
            None
        )

        login(request, user)

        return redirect('feed')

    return render(
        request,
        'users/verify_otp.html'
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('feed')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'users/login.html',
        {'form': form}
    )


def logout_view(request):

    logout(request)

    return redirect('home')