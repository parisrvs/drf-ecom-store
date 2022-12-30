"""
Test models for products app.
"""

from django.test import TestCase
from django.utils.text import slugify
from core.products.models import (
    Collection,
)


class TestModels(TestCase):

    def test_create_collection_return_200(self):
        payload = {
            "title": "test title",
            "slug": slugify("test title")
        }

        collection = Collection.objects.create(**payload)

        self.assertEqual(collection.title, payload["title"])
        self.assertEqual(collection.slug, payload["slug"])
