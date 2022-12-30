from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, urlencode
from django.db.models import Count, Value
from django.db.models.functions import Concat
from django.urls import reverse
from .models import User, Address


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "username")
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name"
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "count_of_orders",
        "net_worth"
    )
    ordering = ("first_name", "last_name")
    list_per_page = 10

    @admin.display(ordering="count_of_orders")
    def count_of_orders(self, user):
        url = reverse("admin:orders_order_changelist") + '?' + urlencode({
            "user__id": str(user.id)
        })
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            user.count_of_orders
        )

    def net_worth(self, user):
        net_worth = 0
        for order in user.orders.all():
            order_total = 0
            for orderitem in order.items.all():
                price = orderitem.product.price * orderitem.quantity
                discount = 0 if not orderitem.product.discount else orderitem.product.discount
                discounted_price = price - (price * (discount/100))
                order_total += discounted_price

            discount = 0 if not order.discount else order.discount.percent
            discounted_price = order_total - (order_total * (discount/100))
            net_worth += discounted_price
        return round(net_worth)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count_of_orders=Count("orders")
        ).prefetch_related(
            "orders__items__product",
            "orders__discount"
        )


class AddressAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = [
        "id", "full_name", "address1", "mobile",
        "city", "state", "pincode", "country",
        "count_of_orders"
    ]
    autocomplete_fields = ["user"]
    search_fields = [
        "first_name__istartswith", "last_name__istartswith",
        "city", "state", "pincode"
    ]
    list_select_related = ["user"]

    @admin.display(ordering="count_of_orders")
    def count_of_orders(self, address):
        url = reverse("admin:orders_order_changelist") + '?' + urlencode({
            "address__id": str(address.id)
        })
        return format_html("<a href='{}'>{}</a>", url, address.count_of_orders)

    @admin.display(ordering="full_name")
    def full_name(self, address):
        url = reverse("admin:accounts_user_change", args=(address.user.id,))
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            address.full_name
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count_of_orders=Count("orders"),
            full_name=Concat("first_name", Value(' '), "last_name")
        )


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
