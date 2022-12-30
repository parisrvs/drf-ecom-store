from django.core.management.base import BaseCommand
from typing import Any, Optional
from ._private import (
    destroy_collection,
    destroy_variations,
    destroy_discounts,
    destroy_tags,
    destroy_products,
    destroy_pincodes,
    destroy_users,
    destroy_reviews,
    destroy_address,
    destroy_orders
)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        # destroy_orders()
        # destroy_address()
        # destroy_reviews()
        # destroy_users()
        # destroy_pincodes()
        # destroy_products()
        # destroy_discounts()
        # destroy_tags()
        # destroy_variations()
        # destroy_collection()
        pass
