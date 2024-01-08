from .models import User, HealthRecord
from .serializers import UserSerializer, HealthRecordSerializer
from rest_framework import viewsets
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials, auth
import json
import requests
import datetime
import logging
from datetime import  timedelta


logger = logging.getLogger(__name__)

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate('healthcare-408423-firebase-adminsdk-znfbz-bb55f1ca6a.json')
    firebase_admin.initialize_app(cred)

@csrf_exempt
def send_token_to_google_fit(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        firebase_id_token = data.get('firebaseIdToken')
        decoded_token = auth.verify_id_token(firebase_id_token)
        user_id = decoded_token['uid']
        
        # Instead of redirecting, send back the Google OAuth URL
        google_oauth_url = get_google_auth_url(request)
        return JsonResponse({'google_oauth_url': google_oauth_url})

    except Exception as e:
        logger.error(f"Error in Firebase token verification: {e}")
        return JsonResponse({'message': 'Error', 'error': str(e)}, status=500)

def get_google_auth_url(request):
    """Generate Google OAuth URL."""
    google = OAuth2Session(settings.GOOGLE_CLIENT_ID, redirect_uri=settings.GOOGLE_REDIRECT_URI, scope=settings.GOOGLE_SCOPE)
    authorization_url, state = google.authorization_url(settings.GOOGLE_AUTHORIZATION_URL)
    
    request.session['oauth_state'] = state
    return authorization_url



def google_login(request):
    google = OAuth2Session(settings.GOOGLE_CLIENT_ID, redirect_uri=settings.GOOGLE_REDIRECT_URI, scope=settings.GOOGLE_SCOPE)
    authorization_url, state = google.authorization_url(settings.GOOGLE_AUTHORIZATION_URL)
    
    # Log the authorization URL
    print("Authorization URL:", authorization_url)  # Add this line
    logger.info("Authorization URL: %s", authorization_url)
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def fetch_google_fit_data(access_token, data_type):
    now = datetime.datetime.now()
    one_week_ago = now - datetime.timedelta(days=7)
    start_time_millis = int(one_week_ago.timestamp()) * 1000
    end_time_millis = int(now.timestamp()) * 1000

    headers = {'Authorization': 'Bearer ' + access_token}

    # Handling for aggregated data types
    data_request = {
        "aggregateBy": [{"dataTypeName": data_type}],
        "bucketByTime": {"durationMillis": 86400000},  # Aggregating data daily
        "startTimeMillis": start_time_millis,
        "endTimeMillis": end_time_millis
    }
    response = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers=headers, json=data_request)

    return response.json()

def aggregate_data_weekly(google_fit_data):
    # Initialize a dictionary to store weekly aggregated data
    weekly_aggregated_data = {}

    # Process each data type
    for data_type, data in google_fit_data.items():
        for bucket in data["bucket"]:
            # Extract start time of the bucket
            start_time = datetime.datetime.fromtimestamp(int(bucket["startTimeMillis"]) / 1000)
            week_start = start_time - datetime.timedelta(days=start_time.weekday())
            week_start_str = week_start.strftime('%Y-%m-%d')  # Format datetime as string

            # Initialize weekly data
            if week_start_str not in weekly_aggregated_data:
                weekly_aggregated_data[week_start_str] = {
                    "active_minutes": 0,
                    "calories_expended": 0,
                    "step_count_delta": 0
                }

            # Aggregate data
            for dataset in bucket["dataset"]:
                for point in dataset["point"]:
                    value = point["value"][0]
                    if data_type == "com.google.active_minutes":
                        weekly_aggregated_data[week_start_str]["active_minutes"] += value.get("intVal", 0)
                    elif data_type == "com.google.step_count.delta":
                        weekly_aggregated_data[week_start_str]["step_count_delta"] += value.get("intVal", 0)
                    elif data_type == "com.google.calories.expended":
                        weekly_aggregated_data[week_start_str]["calories_expended"] += value.get("fpVal", 0.0)

    return weekly_aggregated_data

def google_callback(request):
    try:
        # Create an OAuth session to fetch the token
        google = OAuth2Session(settings.GOOGLE_CLIENT_ID, redirect_uri=settings.GOOGLE_REDIRECT_URI)
        token = google.fetch_token(
            settings.GOOGLE_TOKEN_URL,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri()
        )

        # Here, you might want to use the token to fetch user data or create a session

        # Redirect to the frontend application's homepage/dashboard
        return redirect('http://localhost:8080/')  # Update with the actual URL of your frontend

    except Exception as e:
        # Handle exceptions and errors
        logger.error(f"Error during Google OAuth callback: {e}")
        return JsonResponse({'error': str(e)}, status=500)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer