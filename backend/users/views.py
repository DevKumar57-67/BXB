from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import RegistrationForm
from .models import User, EmailOTP
from .utils import send_otp_email


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Support either:
            # password
            # or Django-style password1
            password = (
                form.cleaned_data.get("password")
                or form.cleaned_data.get("password1")
            )

            if not password:
                form.add_error(
                    None,
                    "Password field is missing from the registration form."
                )

                return render(
                    request,
                    "users/register.html",
                    {"form": form}
                )

            # Store registration information temporarily
            # until email OTP verification is completed.
            request.session["registration_data"] = {
                "username": username,
                "email": email,
                "password": password,
            }

            # Send OTP to registration email
            send_otp_email(email)

            return redirect("verify_otp")

    else:
        form = RegistrationForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form
        }
    )


def verify_otp(request):
    registration_data = request.session.get(
        "registration_data"
    )

    if not registration_data:
        return redirect("register")

    if request.method == "POST":

        otp = request.POST.get(
            "otp",
            ""
        ).strip()

        otp_record = (
            EmailOTP.objects
            .filter(
                email=registration_data["email"],
                verified=False
            )
            .order_by("-created_at")
            .first()
        )

        if not otp_record:
            return render(
                request,
                "users/verify_otp.html",
                {
                    "error":
                        "OTP not found. Please request a new OTP."
                }
            )

        if otp_record.expires_at < timezone.now():
            return render(
                request,
                "users/verify_otp.html",
                {
                    "error":
                        "OTP has expired. Please request a new OTP."
                }
            )

        if otp_record.attempts >= 5:
            return render(
                request,
                "users/verify_otp.html",
                {
                    "error":
                        "Too many attempts. Please request a new OTP."
                }
            )

        if otp != otp_record.otp:

            otp_record.attempts += 1
            otp_record.save(
                update_fields=["attempts"]
            )

            return render(
                request,
                "users/verify_otp.html",
                {
                    "error":
                        "Invalid OTP. Please try again."
                }
            )

        # OTP is correct
        otp_record.verified = True
        otp_record.save(
            update_fields=["verified"]
        )

        # Create account only after successful OTP verification
        user = User.objects.create_user(
            username=registration_data["username"],
            email=registration_data["email"],
            password=registration_data["password"],
        )

        # Clear temporary registration data
        request.session.pop(
            "registration_data",
            None
        )

        # Log the user in
        login(
            request,
            user
        )

        return redirect("feed")

    return render(
        request,
        "users/verify_otp.html"
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("feed")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "users/login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    logout(request)

    return redirect("home")