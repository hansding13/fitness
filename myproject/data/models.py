from django.db import models
from django.conf import settings

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    google_id = models.CharField(max_length=100, unique=True, null=True)
    google_access_token = models.CharField(max_length=255, null=True)

class FitnessData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_starting = models.DateField()  # Identifies the starting date of the week
    active_minutes = models.IntegerField(default=0)
    calories_expended = models.FloatField(default=0.0)
    step_count_delta = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'week_starting']  # Ensures uniqueness for each week's data per user

class HealthRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    record_date = models.DateField()  # Date of the health record
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    # Other health metrics can be added here
