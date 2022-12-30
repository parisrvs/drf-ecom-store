from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# from django.utils.html import format_html, urlencode
# from django.db.models import Count, Value
# from django.urls import reverse
from .models import User


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
        # "count_of_orders",
        # "net_worth"
    )
    ordering = ("first_name", "last_name")
    list_per_page = 10

    # @admin.display(ordering="count_of_orders")
    # def count_of_orders(self, user):
    #     url = reverse("admin:orders_order_changelist") + '?' + urlencode({
    #         "user__id": str(user.id)
    #     })
    #     return format_html(
    #         "<a href='{}'>{}</a>",
    #         url,
    #         user.count_of_orders
    #     )

    # def net_worth(self, user):
    #     net_worth = 0
    #     for order in user.orders.all():
    #         order_total = 0
    #         for orderitem in order.items.all():
    #             price = orderitem.product.price * orderitem.quantity
    #             discount = 0 if not orderitem.product.discount else orderitem.product.discount # noqa
    #             discounted_price = price - (price * (discount/100))
    #             order_total += discounted_price

    #         discount = 0 if not order.discount else order.discount.percent
    #         discounted_price = order_total - (order_total * (discount/100))
    #         net_worth += discounted_price
    #     return round(net_worth)

    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         count_of_orders=Count("orders")
    #     ).prefetch_related(
    #         "orders__items__product",
    #         "orders__discount"
    #     )


admin.site.register(User, UserAdmin)
