from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser

class AuthTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="12345",
            role="OPERADOR"
        )
        self.login_url = reverse('custom_token_obtain_pair')

    def test_login_jwt_success(self):
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "12345"
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_jwt_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "wrongpass"
        }, format="json")

        self.assertEqual(response.status_code, 401)
