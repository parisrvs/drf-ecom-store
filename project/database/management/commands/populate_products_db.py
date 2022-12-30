from django.core.management.base import BaseCommand
from typing import Any, Optional
from ._private import (
    create_collections,
    create_variations,
    create_discounts,
    create_tags,
    create_products,
    create_pincodes,
    create_users,
    create_reviews,
    create_address,
    create_orders
)


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        # create_collections()
        # create_variations()
        # create_tags()
        # create_discounts()
        # create_products()
        # create_pincodes()
        # create_users()
        # create_reviews()
        # create_address()
        # create_orders()
        pass
