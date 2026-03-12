from django.urls import path
from users.api.views import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
]