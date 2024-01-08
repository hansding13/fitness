from rest_framework import serializers
from .models import User
from .models import HealthRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'user', 'blood_pressure', 'heart_rate', 'blood_glucose', 'body_temperature', 'oxygen_saturation', 'steps_count', 'sleep_pattern', 'water_intake', 'medication_intake', 'doctor_visits', 'vaccinations', 'record_data']
