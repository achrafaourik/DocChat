"""
Create tests for testing that the user API works properly
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public unauthenticated user API endpoints"""

    def setUp(self):
        """Setup the public unauthenticated user API endpoints"""
        self.client = APIClient()

    def test_create_user_sucess(self):
        """Test that the create user API endpoint works properly"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_same_email_error(self):
        """Test that creating a user with an existing email fails"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "test user",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test that creating a user with a short password fails"""
        payload = {"email": "test@example.com",
                   "password": "12", "name": "test user"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token creation API works properly for valid credentials."""
        user_details = {
            "email": "user@example.com",
            "password": "password123456",
            "name": "user_name",
        }
        create_user(**user_details)

        payload = {"email": user_details["email"],
                   "password": user_details["password"]}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_bad_credentials(self):
        """Test that creating a token with invalid credentials is not allowed"""
        user_details = {
            "email": "user@example.com",
            "password": "password123456",
            "name": "user_name",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": "wrongpassword123456",
        }

        res = self.client.post(TOKEN_URL, payload=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("tokan", res.data)

    def test_create_token_blank_password(self):
        """Test that creating a token with blank password returns error"""
        payload = {
            "email": "test@example.com",
            "password": "",
        }

        res = self.client.post(TOKEN_URL, payload=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("tokan", res.data)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email="test@example.com", password="password123456", name="test name"
        )
        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_sucess(self):
        """Test retrieving profile successful for logged in users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {"email": self.user.email, "name": self.user.name})

    def test_post_me_not_allowed(self):
        """Test that POST request not allowed"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile"""
        payload = {"name": "new name", "password": "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
