from django.utils.text import slugify
from datetime import datetime, timedelta, timezone
from . import _utils as db_utils
from core.products.models import (
    Collection,
    Key,
    Value,
    Variation,
    Tag,
    Discount,
    Product,
    Image,
    Pincode,
    Review
)

from core.accounts.models import (
    User,
)

import random


def create_collections():
    titles = []
    for _ in range(100):
        while True:
            title = db_utils.get_category_collection_title()
            if title not in titles:
                titles.append(title)
                break

        c = Collection.objects.create(
            title=title,
            slug=slugify(title)
        )
    return


def destroy_collection():
    Collection.objects.all().delete()
    return


def create_variations():
    keys = []
    keys_objs = {}
    values = []
    for _ in range(20):
        while True:
            key = db_utils.get_tag_name()
            if key not in keys:
                keys.append(key)
                break

        k = Key.objects.create(
            key=key
        )
        keys_objs[k] = []

        for _ in range(random.randint(6, 10)):
            while True:
                value = db_utils.get_tag_name()
                if value not in values:
                    values.append(value)
                    break

            v = Value.objects.create(
                value=value
            )
            (keys_objs[k]).append(v)

    for key, values in keys_objs.items():
        for value in values:
            v = Variation.objects.create(
                key=key,
                value=value
            )

    return


def destroy_variations():
    Variation.objects.all().delete()
    Value.objects.all().delete()
    Key.objects.all().delete()
    return


def create_tags():
    tags = []
    for _ in range(100):
        while True:
            tag = db_utils.get_tag_name()
            if tag not in tags:
                tags.append(tag)
                break

        Tag.objects.create(
            tag=tag,
            slug=slugify(tag)
        )
    return


def destroy_tags():
    Tag.objects.all().delete()
    return


def create_discounts():
    codes = []
    for _ in range(10):
        while True:
            code = db_utils.get_tag_name()
            if code not in codes:
                codes.append(code)
                break

        d = Discount.objects.create(
            code=code,
            percent=random.randint(5, 30)
        )

    return


def destroy_discounts():
    Discount.objects.all().delete()
    return


def create_products():
    collections = Collection.objects.all()
    all_images = Image.objects.all()
    all_variations = Variation.objects.all()
    all_tags = Tag.objects.all()
    titles = []

    for _ in range(1000):
        unit = random.choice(["Kg", "Pc", "Dz", "Lt"])
        variations = []
        tags = []
        images = []
        while True:
            title = db_utils.get_product_title()
            if title not in titles:
                titles.append(title)
                break

        t = random.randint(1, 100)
        created_at = datetime.now(timezone.utc) - timedelta(days=t)

        discount = None
        if random.choice([True, False]):
            discount = random.randint(10, 50)

        p = Product.objects.create(
            collection=random.choice(collections),
            title=title,
            slug=slugify(title),
            price=random.randint(100, 1000),
            discount=discount,
            unit=unit,
            description=db_utils.get_product_info(),
            delivery_time_in_days=random.randint(1, 3),
            created_at=created_at.replace(tzinfo=timezone.utc)
        )

        for _ in range(random.randint(0, 5)):
            while True:
                variation = random.choice(all_variations)
                if variation not in variations:
                    variations.append(variation)
                    break
            p.variations.add(variation)

        for _ in range(random.randint(2, 5)):
            while True:
                image = random.choice(all_images)
                if image not in images:
                    images.append(image)
                    break
            p.images.add(image)

        for _ in range(2, 5):
            while True:
                tag = random.choice(all_tags)
                if tag not in tags:
                    tags.append(tag)
                    break
            p.tags.add(tag)

    return


def destroy_products():
    Product.objects.all().delete()
    return


def create_pincodes():
    all_products = Product.objects.all()
    pincodes = []
    for _ in range(1000):
        products = []
        while True:
            pincode = db_utils.get_digits(6)
            if pincode not in pincodes:
                pincodes.append(pincode)
                break

        pincode = Pincode.objects.create(
            pincode=pincode,
            delivery_time_in_days=random.randint(1, 5)
        )

        if random.choice([True, False]):
            for _ in range(random.randint(5, 10)):
                while True:
                    product = random.choice(all_products)
                    if product not in products:
                        products.append(product)
                        break
            for product in products:
                pincode.products_not_available.add(product)
    return


def destroy_pincodes():
    p = Pincode.objects.all().delete()
    return


def create_users():
    password = "qwerty*1"
    usernames = []
    for _ in range(100):
        first_name = db_utils.get_tag_name()
        last_name = db_utils.get_tag_name()
        while True:
            username = db_utils.get_tag_name()
            if username not in usernames:
                usernames.append(username)
                break

        u = User.objects.create_user(
            username=username.strip().lower(),
            email=f"{username.strip().lower()}@example.com",
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        u.save()

    return


def destroy_users():
    User.objects.all().exclude(is_staff=True).delete()
    return


def create_reviews():
    products = Product.objects.all()
    all_users = User.objects.all().exclude(is_staff=True)
    for product in products:
        users = []
        for _ in range(random.randint(5, 10)):
            while True:
                user = random.choice(all_users)
                if user not in users:
                    users.append(user)
                    break

            t = random.randint(1, 90)
            created_at = datetime.now(timezone.utc) - timedelta(days=t)
            r = Review.objects.create(
                product=product,
                user=user,
                description=db_utils.get_product_info(),
                created_at=created_at.replace(tzinfo=timezone.utc),
                rating=random.randint(1, 5)
            )

    return


def destroy_reviews():
    Review.objects.all().delete()
    return
