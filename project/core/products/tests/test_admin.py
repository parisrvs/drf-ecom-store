"""
Test django admin site for products app.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from core.accounts.models import User
from core.products import models


class AdminSiteTest(TestCase):
    """tests for django admin."""

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="ILoveDjango",
            username="admin",
            first_name="Vasudeva",
            last_name="Krishna"
        )
        self.client.force_login(self.admin_user)

    def test_collections_list(self):
        """Test collections list page."""

        url = reverse("admin:products_collection_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_edit_collections_page(self):
        """Test collection item page."""

        collection = models.Collection.objects.create(
            title="test title",
            slug=slugify("test title")
        )
        url = reverse("admin:products_collection_change", args=[collection.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_collections_page(self):
        """Test add collection item page."""

        url = reverse("admin:products_collection_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
