import random
import string


def get_category_collection_title():
    title1 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(4, 7)))
    title2 = ''.join(random.choices(string.ascii_lowercase +
                     string.digits, k=random.randint(0, 2)))

    if not title2:
        title = f"{title1.strip()}"
    else:
        title = f"{title1} {title2}"
    return title.strip().title()


def get_tag_name():
    title = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(4, 7)))
    return title.strip().title()


def get_product_title():
    title1 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(4, 7)))
    title2 = ''.join(random.choices(string.ascii_lowercase +
                     string.digits, k=random.randint(0, 2)))
    title3 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(0, 3)))

    if not title2 and not title3:
        title = f"{title1.strip()}"
    elif not title2:
        title = f"{title1} {title3}"
    elif not title3:
        title = f"{title1} {title2}"
    else:
        title = f"{title1} {title2} {title3}"

    return title.strip().title()


def get_product_info():
    sentences = ''
    for _ in range(random.randint(3, 8)):
        words = ''
        for _ in range(random.randint(4, 15)):
            words = words + \
                ''.join(random.choices(string.ascii_lowercase,
                        k=random.randint(2, 8))) + ' '

        words = words.strip() + '. '
        sentences += words.capitalize()
    return sentences.strip()


def get_digits(n):
    digits = ''.join(random.choices(string.digits, k=n))
    return digits


def get_address1():
    number = ''.join(random.choices(string.digits, k=random.randint(1, 3)))
    text1 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(5, 10)))
    text2 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(7, 12)))

    address = f"{number}, {text1.strip().title()}, {text2.strip().title()}"
    return address


def get_address2():
    text1 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(5, 10)))
    text2 = ''.join(random.choices(
        string.ascii_lowercase, k=random.randint(7, 12)))

    address = f"{text1.strip().title()}, {text2.strip().title()}"
    return address
