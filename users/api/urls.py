from django.urls import path
from users.api.views import RegistrationView, LoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
]