from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class CreateAccountTests(APITestCase):

    def test_create_account_201(self):
        url = reverse('register')
        data = {
            "fullname": "Example Username",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }  
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_400(self):
        url = reverse('register')
        data = {
            "fullname": "Example Username",
            "email": "example@mail.de",
            "password": "examplePassword"
        }  
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            fullname='Test User',
            email='test@example.com',
            password='password123',
        )
        self.client.force_authenticate(user=self.user)

    def test_login_200(self):
        url = reverse('login')
        data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_400(self):
        url = reverse('login')
        data = {
            "email": "test@example.com",
            "password": "password"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)