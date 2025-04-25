from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .models import FileUpload
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .utils import generate_otp, send_otp_email, otp_is_valid

User = get_user_model()

# Store OTPs and their expiration time
otp_data = {}

# Login using Email and Password
def login_password(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('upload_file')  # Redirect after successful login
        else:
            messages.error(request, "Invalid credentials. Please check your email and password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'active_tab': 'emailPassword'})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        auth_method = request.POST.get('auth_method')
        
        # Email-based OTP authentication
        if auth_method == 'otp':
            if email in otp_data:
                otp = otp_data[email]['otp']
                otp_time = otp_data[email]['otp_time']
                entered_otp = request.POST.get('otp')
                
                # Validate OTP
                if otp_is_valid(otp_time, otp) and int(entered_otp) == otp:
                    user = User.objects.get(email=email)
                    login(request, user)
                    del otp_data[email]  # Clear OTP after successful login
                    return redirect('upload_file')
                else:
                    messages.error(request, "Invalid or expired OTP. Please request a new one.")
            else:
                messages.error(request, "No OTP found. Please request one.")
            return redirect('login')
        
        # Email/password authentication
        elif auth_method == 'password':
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('upload_file')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    
    return render(request, 'registration/login.html')

def request_otp(request):
    """Generate OTP and send via email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            send_otp_email(email, otp)
            otp_data[email] = {'otp': otp, 'otp_time': timezone.now()}
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')
        except ObjectDoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('request_otp')
    
    return render(request, 'authentication/request_otp.html')

def verify_otp(request):
    """Verify the OTP entered by the user"""
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')

        if email in otp_data:
            otp_info = otp_data[email]
            otp = otp_info['otp']
            otp_time = otp_info['otp_time']

            # Check if the entered OTP is correct and if it is still valid
            if otp == int(entered_otp) and otp_is_valid(otp_time, otp):
                # Login the user
                user = User.objects.get(email=email)
                login(request, user)
                del otp_data[email]  # Clear OTP after successful login
                return redirect('upload_file')
            else:
                messages.error(request, "Invalid or expired OTP. Please try again.")
                return redirect('verify_otp')

        else:
            messages.error(request, "OTP not found. Request a new OTP.")
            return redirect('request_otp')
    
    return render(request, 'authentication/verify_otp.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in automatically after registration
            return redirect('upload_file')  # Redirect to the upload page
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        user_email = request.user.email
        FileUpload.objects.create(user_email=user_email, file=file)
        return redirect('user_uploads')
    
    return render(request, 'upload_form.html')

@login_required
def user_uploads(request):
    uploads = FileUpload.objects.filter(user_email=request.user.email)
    return render(request, 'user_uploads.html', {'uploads': uploads})

