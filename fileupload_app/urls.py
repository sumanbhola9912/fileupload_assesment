from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('request_otp/', views.request_otp, name='request_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),
    path('login-password/', views.login_password, name='login_password'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('uploads/', views.user_uploads, name='user_uploads'),
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),
]