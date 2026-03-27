from django.urls import path
from users.api.views import RegistrationView, LoginView, EmailCheckView

# Define the URL patterns for the user-related API endpoints
urlpatterns = [
    # Endpoint for new user registration: /api/users/registration/
    path('registration/', RegistrationView.as_view(), name='register'),
    
    # Endpoint for user login and token generation: /api/users/login/
    path('login/', LoginView.as_view(), name='login'),
    
    # Endpoint to verify if an email exists and get user details: /api/users/email-check/
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]