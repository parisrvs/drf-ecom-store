from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.accounts.models import User
from core.products.validators import validate_file_size


class Collection(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Key(models.Model):
    key = models.CharField(max_length=128, unique=True)
    values = models.ManyToManyField("Value", through="Variation")

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return self.key


class Value(models.Model):
    value = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "value"
        ordering = ["value"]


class Variation(models.Model):
    key = models.ForeignKey(
        Key,
        on_delete=models.CASCADE,
        related_name='variations'
    )
    value = models.ForeignKey(
        Value,
        on_delete=models.CASCADE,
        related_name='+'
    )

    def __str__(self):
        return f"{self.key} - {self.value}"

    class Meta:
        unique_together = [['key', 'value']]
        ordering = ["key"]


class Tag(models.Model):
    tag = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ["tag"]

    def __str__(self):
        return self.tag


class Image(models.Model):
    image = models.ImageField(
        upload_to="images/product-images/",
        validators=[validate_file_size]
    )
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    code = models.CharField(max_length=128, unique=True)
    percent = models.IntegerField()

    def __str__(self):
        return self.code


class Product(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name="products",
    )
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    price = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    discount = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=10)
    availability = models.BooleanField(default=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    variations = models.ManyToManyField(
        Variation,
        blank=True,
        related_name="products"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    images = models.ManyToManyField(Image, blank=True, related_name="+")
    created_at = models.DateTimeField(default=timezone.now)
    inventory = models.IntegerField(default=100)
    delivery_time_in_days = models.IntegerField(default=1)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )
    description = models.TextField(max_length=1024)
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [['product', 'user']]
        ordering = ["-created_at"]


class Pincode(models.Model):
    pincode = models.CharField(max_length=50, unique=True)
    products_not_available = models.ManyToManyField(
        Product,
        blank=True,
        related_name="+"
    )
    delivery_time_in_days = models.IntegerField(default=1)

    def __str__(self):
        return self.pincode
