from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from uuid import uuid4
from core.accounts.models import Address, User
from core.products.models import Discount, Product


class Order(models.Model):
    OPEN = "OP"
    CLOSED = "CL"
    CANCELLED = "CN"
    PENDING_CANCELLATION = "PC"

    ORDER_STATUS_CHOICES = [
        (OPEN, "OPEN"),
        (CLOSED, "CLOSED"),
        (CANCELLED, "CANCELLED"),
        (PENDING_CANCELLATION, "PENDING CANCELLATION")
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    order_status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=OPEN
    )
    created_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_request_at = models.DateTimeField(blank=True, null=True)
    expected_delivery_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='items'
    )
    quantity = models.FloatField()

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartDetail(models.Model):
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        related_name="detail"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True
    )
    discount_percent = models.IntegerField(blank=True, null=True)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    discount_code = models.CharField(max_length=128, blank=True, null=True)
    availability = models.BooleanField(default=True)
    amount_payable = models.IntegerField(blank=True, null=True)
    expected_delivery_time = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = [["user", "address"]]


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='+'
    )
    quantity = models.FloatField(validators=[MinValueValidator(1)])
    availability = models.BooleanField(default=True)

    class Meta:
        unique_together = [["cart", "product"]]
