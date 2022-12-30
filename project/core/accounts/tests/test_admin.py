"""
Test for django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """test for django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
            username="admin",
            first_name="firstname",
            last_name="lastname"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            first_name="firstname",
            last_name="lastname",
            username="user"
        )

    def test_users_list(self):
        """test that users are listed on page."""
        url = reverse("admin:accounts_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that edit user page works correctly."""
        url = reverse("admin:accounts_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """Test the create user page works."""

        url = reverse("admin:accounts_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
