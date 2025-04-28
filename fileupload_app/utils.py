# fileupload_app/utils.py
import random
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

def generate_otp():
    # Generate a random 6-digit OTP
    otp = random.randint(100000, 999999)
    return otp

def send_otp_email(user_email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])

def otp_is_valid(otp_time, otp):
    """Check if the OTP is still valid (valid for 5 minutes)"""
    expiration_time = otp_time + timedelta(minutes=5)
    return timezone.now() <= expiration_time
