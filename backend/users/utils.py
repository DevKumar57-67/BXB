import random
from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone

from .models import EmailOTP


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email):

    otp = generate_otp()

    expires_at = timezone.now() + timedelta(minutes=5)

    EmailOTP.objects.filter(
        email=email,
        verified=False
    ).delete()

    EmailOTP.objects.create(
        email=email,
        otp=otp,
        expires_at=expires_at
    )

    send_mail(
        subject='Your BxB Email Verification OTP',
        message=(
            f'Your BitsXBytes verification OTP is: {otp}\n\n'
            'This OTP is valid for 5 minutes.\n'
            'Do not share this OTP with anyone.'
        ),
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )