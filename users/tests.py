from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:create")
        self.token_url = reverse("user:token_obtain_pair")
        self.refresh_url = reverse("user:token_refresh")
        self.verify_url = reverse("user:token_verify")
        self.me_url = reverse("user:manage")

        self.user_data = {
            "email": "test@example.com",
            "password": "password123",
        }

        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_token_obtain_pair(self):
        response = self.client.post(self.token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        response = self.client.post(self.token_url, self.user_data)
        refresh_token = response.data["refresh"]

        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verify(self):
        response = self.client.post(self.token_url, self.user_data)
        access_token = response.data["access"]

        response = self.client.post(self.verify_url, {"token": access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user(self):
        response = self.client.post(self.token_url, self.user_data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_update_current_user(self):
        response = self.client.post(self.token_url, self.user_data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        update_data = {"first_name": "Updated", "last_name": "User"}
        response = self.client.patch(self.me_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
