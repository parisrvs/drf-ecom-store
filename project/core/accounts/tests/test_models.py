"""
Tests for models.
"""

from django.test import TestCase
from core.accounts.models import User


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_return_success(self):
        """Test creating a user successful."""

        payload = {
            "username": "user",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "test@example.com",
            "password": "ILoveDjango"
        }

        user = User.objects.create_user(**payload)

        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com", "user1"],
            ["Test2@Example.com", "Test2@example.com", "user2"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com", "user3"],
            ["test4@example.COM", "test4@example.com", "user4"]
        ]

        for email, expected_email, username in sample_emails:
            payload = {
                "first_name": "firstname",
                "last_name": "lastname",
                "password": "ILoveDjango",
                "email": email,
                "username": username
            }
            user = User.objects.create_user(**payload)
            self.assertEqual(user.email, expected_email)
