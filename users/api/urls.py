from django.urls import path
from users.api.views import RegistrationView, LoginView, EmailCheckView

# URL configuration for User Authentication and Management.
# These endpoints are typically prefixed with 'api/' in the main urls.py.

urlpatterns = [
    # POST: Register a new user and receive an Auth Token.
    path('registration/', RegistrationView.as_view(), name='register'),

    # POST: Login with Email/Password and receive an Auth Token.
    path('login/', LoginView.as_view(), name='login'),

    # GET: Verify if an email exists (Used for adding members to boards).
    path('email-check/', EmailCheckView.as_view(), name='email_check'),
]