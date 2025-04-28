"""
URL configuration for fileupload project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import LoginView
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


# Custom view to handle redirect for logged-in users
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('user_uploads')  # Redirect to the 'upload' page if already logged in
    return auth_views.LoginView.as_view()(request)  # Show login page if not logged in

urlpatterns = [
    path('', home_redirect, name='home'),  # Root URL with login check
    path('admin/', admin.site.urls),  # Admin panel URL
    path('upload/', include('fileupload_app.urls')),  # App-specific URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
