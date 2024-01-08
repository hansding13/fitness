from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import UserViewSet, HealthRecordViewSet
from . import views
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'healthrecords', HealthRecordViewSet)


urlpatterns = [
    path('', include(router.urls)),
]