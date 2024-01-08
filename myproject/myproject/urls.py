"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from data.views import google_login, google_callback,send_token_to_google_fit   # Import these functions
from data import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google/login/', google_login, name='google_login'),  # Google login URL
    path('google/callback/', google_callback, name='google_callback'),  # Google callback URL
    path('', include('data.urls')),  # Include URLs from the data app
    path('api/send-token/',send_token_to_google_fit, name='send_token_to_google_fit'),

]



