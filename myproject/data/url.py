from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('user/', views.user_view, name='user_view'),
    # You can add more URL patterns here as needed
]
