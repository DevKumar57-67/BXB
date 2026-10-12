from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegistrationForm
from .models import EmailOTP, User
from .utils import send_otp_email


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data.get("password1") or form.cleaned_data.get("password")

            if not password:
                form.add_error(None, "Password field is missing from the registration form.")
                return render(request, "users/register.html", {"form": form})

            request.session["registration_data"] = {
                "username": username,
                "email": email,
                "password": password,
            }

            send_otp_email(email)
            return redirect("verify_otp")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def verify_otp(request):
    registration_data = request.session.get("registration_data")

    if not registration_data:
        return redirect("register")

    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        otp_record = (
            EmailOTP.objects.filter(email=registration_data["email"], verified=False)
            .order_by("-created_at")
            .first()
        )

        if not otp_record:
            return render(
                request,
                "users/verify_otp.html",
                {"error": "OTP not found. Please request a new OTP."},
            )

        if otp_record.expires_at < timezone.now():
            return render(
                request,
                "users/verify_otp.html",
                {"error": "OTP has expired. Please request a new OTP."},
            )

        if otp_record.attempts >= 5:
            return render(
                request,
                "users/verify_otp.html",
                {"error": "Too many attempts. Please request a new OTP."},
            )

        if otp != otp_record.otp:
            otp_record.attempts += 1
            otp_record.save(update_fields=["attempts"])
            return render(
                request,
                "users/verify_otp.html",
                {"error": "Invalid OTP. Please try again."},
            )

        otp_record.verified = True
        otp_record.save(update_fields=["verified"])

        user = User.objects.create_user(
            username=registration_data["username"],
            email=registration_data["email"],
            password=registration_data["password"],
        )

        request.session.pop("registration_data", None)
        login(request, user)
        return redirect("feed")

    return render(request, "users/verify_otp.html")


def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.user.is_authenticated:
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect("feed")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("feed")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "users/login.html",
        {"form": form, "next": next_url or ""},
    )


def logout_view(request):
    logout(request)
    return redirect("home")
