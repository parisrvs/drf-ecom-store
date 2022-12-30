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
    Address
)

from core.orders.models import (
    Order,
    OrderItem
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


def create_address():
    all_pincodes = Pincode.objects.all()
    states = {db_utils.get_tag_name(): {} for _ in range(2)}
    cities = []
    pincodes = []
    country = db_utils.get_tag_name()
    mobiles = []
    for state in states.keys():
        for _ in range(random.randint(10, 20)):
            while True:
                city = db_utils.get_tag_name()
                if city not in cities:
                    cities.append(city)
                    break
            states[state][city] = []

            for _ in range(random.randint(10, 20)):
                while True:
                    pincode = random.choice(all_pincodes)
                    if pincode not in pincodes:
                        pincodes.append(pincode)
                        break
                states[state][city].append(pincode)

    addresses = []
    for state, cities in states.items():
        for city, pincodes in cities.items():
            for pincode in pincodes:
                landline = db_utils.get_digits(
                    10) if random.choice([True, False]) else None

                address2 = db_utils.get_address2() if random.choice([
                    True, False]) else None

                while True:
                    mobile = db_utils.get_digits(11)
                    if mobile not in mobiles:
                        mobiles.append(mobile)
                        break

                addresses.append({
                    "mobile": mobile,
                    "landline": landline,
                    "address1": db_utils.get_address1(),
                    "address2": address2,
                    "landmark": db_utils.get_tag_name(),
                    "pincode": pincode.pincode,
                    "city": city,
                    "state": state,
                    "country": country
                })

    total_addresses = len(addresses)
    counter = total_addresses // 100
    index = 0

    users = User.objects.all().exclude(is_staff=True)
    for user in users:
        for _ in range(random.randint(1, counter)):
            Address.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                mobile=addresses[index]["mobile"],
                landline=addresses[index]["landline"],
                address1=addresses[index]["address1"],
                address2=addresses[index]["address2"],
                landmark=addresses[index]["landmark"],
                pincode=addresses[index]["pincode"],
                city=addresses[index]["city"],
                state=addresses[index]["state"],
                country=addresses[index]["country"]
            )
            index += 1
    return


def destroy_address():
    a = Address.objects.all().delete()
    return


def create_orders():
    users = User.objects.all().exclude(is_staff=True)
    all_products = Product.objects.all()
    discount = list(Discount.objects.all())
    discount.append(None)
    orders = {}
    for user in users:
        orders[user] = []
        for _ in range(random.randint(10, 20)):
            products = []
            order = {
                "user": user,
                "address": random.choice(user.address.all()),
                "discount": random.choice(discount),
                "items": []
            }
            for _ in range(random.randint(1, 10)):
                expected_delivery_time = set()
                while True:
                    product = random.choice(all_products)
                    if product not in products:
                        pincode = order["address"].pincode
                        pincode_database = Pincode.objects.filter(
                            pincode=pincode).first()
                        if product not in pincode_database.products_not_available.all():
                            products.append(product)
                            expected_delivery_time.add(
                                product.delivery_time_in_days
                            )
                            expected_delivery_time.add(
                                pincode_database.delivery_time_in_days
                            )
                            break

                order["items"].append({
                    "product": product,
                    "quantity": random.randint(1, 10)
                })
            placed_at = datetime.now(timezone.utc) - \
                timedelta(days=random.randint(0, 50))
            placed_at = placed_at - timedelta(minutes=random.randint(10, 500))
            expected_order_delivery_time = placed_at + \
                timedelta(days=max(expected_delivery_time))
            order["placed_at"] = placed_at
            order["expected_delivery_time"] = expected_order_delivery_time
            orders[user].append(order)

    for user, all_orders in orders.items():
        for order in all_orders:
            status = "OP"
            closed_at = None
            if order["expected_delivery_time"] < datetime.now(timezone.utc):
                closed_at = order["expected_delivery_time"] - \
                    timedelta(minutes=random.randint(60, 500))
                closed_at = closed_at.replace(tzinfo=timezone.utc)
                status = "CL"
            o = Order.objects.create(
                user=user,
                address=order["address"],
                discount=order["discount"],
                created_at=order["placed_at"].replace(tzinfo=timezone.utc),
                expected_delivery_time=order["expected_delivery_time"].replace(
                    tzinfo=timezone.utc),
                order_status=status,
                closed_at=closed_at
            )
            for item in order["items"]:
                oi = OrderItem.objects.create(
                    order=o,
                    product=item["product"],
                    quantity=item["quantity"]
                )

    all_orders = Order.objects.filter(order_status="CL")
    orders = []
    for _ in range(100):
        while True:
            order = random.choice(all_orders)
            if order not in orders:
                orders.append(order)
                break

        order.cancellation_request_at = (
            order.created_at + timedelta(minutes=random.randint(100, 1000))
        ).replace(tzinfo=timezone.utc)
        order.cancelled_at = (
            order.cancellation_request_at +
            timedelta(minutes=random.randint(500, 1000))
        ).replace(tzinfo=timezone.utc)
        order.order_status = "CN"
        order.closed_at = None
        order.save()

    all_orders = Order.objects.filter(order_status="OP")
    orders = []
    for _ in range(5):
        while True:
            order = random.choice(all_orders)
            if order not in orders:
                orders.append(order)
                break

        order.cancellation_request_at = (
            order.created_at + timedelta(minutes=random.randint(500, 1000))
        ).replace(tzinfo=timezone.utc)
        order.order_status = "PC"
        order.save()

    return


def destroy_orders():
    Order.objects.all().delete()
    return
