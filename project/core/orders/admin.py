from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from datetime import timezone, datetime
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    list_select_related = ["product"]
    min_num = 1
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    actions = ["cancel_orders", "close_orders", "request_cancellation"]
    list_display = [
        "id", "customer", "delivery_address", "order_status", "items_count",
        "created_at", "expected_delivery_time", "amount", "discount_percent",
        "amount_payable"
    ]
    list_per_page = 10
    list_select_related = ["user", "discount", "address"]
    autocomplete_fields = ["user", "discount", "address"]
    search_fields = ["id", "user__first_name", "user__last_name"]
    list_filter = ["order_status", "expected_delivery_time"]
    inlines = [OrderItemInline]

    @admin.action(description="Request Cancellation")
    def request_cancellation(self, request, queryset):
        success = 0
        for order in queryset:
            if order.order_status == "OP":
                dt = datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                order.order_status = "PC"
                order.cancellation_request_at = utc_time
                success += 1
                order.save()

        if success == 0:
            self.message_user(
                request,
                "No order was modified.",
                messages.ERROR
            )
        elif success == 1:
            self.message_user(
                request,
                "1 order was successfully updated.",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"{success} orders were successfully updated.",
                messages.SUCCESS
            )

    @admin.action(description="Close Orders")
    def close_orders(self, request, queryset):
        success = 0
        for order in queryset:
            if order.order_status == "OP":
                dt = datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                order.order_status = "CL"
                order.closed_at = utc_time
                success += 1
                order.save()

        if success == 0:
            self.message_user(
                request,
                "No order was modified.",
                messages.ERROR
            )
        elif success == 1:
            self.message_user(
                request,
                "1 order was successfully updated.",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"{success} orders were successfully updated.",
                messages.SUCCESS
            )

    @admin.action(description="Cancel Orders")
    def cancel_orders(self, request, queryset):
        success = 0
        for order in queryset:
            if order.order_status == "PC":
                dt = datetime.now(timezone.utc)
                utc_time = dt.replace(tzinfo=timezone.utc)
                order.order_status = "CN"
                order.cancelled_at = utc_time
                success += 1
                order.save()

        if success == 0:
            self.message_user(
                request,
                "No order was modified.",
                messages.ERROR
            )
        elif success == 1:
            self.message_user(
                request,
                "1 order was successfully updated.",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"{success} orders were successfully updated.",
                messages.SUCCESS
            )

    def delivery_address(self, orderitem):
        url = reverse("admin:accounts_address_change",
                      args=(orderitem.address.id,))
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            orderitem.address
        )

    def customer(self, orderitem):
        url = reverse("admin:accounts_user_change", args=(orderitem.user.id,))
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            orderitem.user.first_name + ' ' + orderitem.user.last_name
        )

    @admin.display(ordering="items_count")
    def items_count(self, order):
        url = reverse("admin:orders_orderitem_changelist") + '?' + urlencode({
            "order__id": str(order.id)
        })
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            order.items_count
        )

    def discount_percent(self, order):
        discount = 0 if not order.discount else order.discount.percent
        return discount

    def amount(self, order):
        total = 0
        for orderitem in order.items.all():
            price = orderitem.product.price * orderitem.quantity
            discount = 0 if not orderitem.product.discount else \
                orderitem.product.discount
            discounted_price = price - (price * (discount/100))
            total += discounted_price
        return round(total)

    def amount_payable(self, order):
        total = self.amount(order)
        discount = 0 if not order.discount else order.discount.percent
        discounted_price = total - (total * (discount/100))
        return round(discounted_price)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count("items")
        ).prefetch_related("items__product")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id", "order_id", "order_item", "quantity",
        "unit_price", "total_price", "discount", "discount_price"
    ]
    list_select_related = ["order", "product"]
    autocomplete_fields = ["order", "product"]
    search_fields = ["order__id", "id"]

    def order_id(self, orderitem):
        url = reverse("admin:orders_order_change", args=(orderitem.order.id,))
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            orderitem.order.id
        )

    def order_item(self, orderitem):
        url = reverse("admin:products_product_change",
                      args=(orderitem.product.id,))
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            orderitem.product
        )

    def unit_price(self, orderitem):
        return orderitem.product.price

    def total_price(self, orderitem):
        return round(orderitem.product.price * orderitem.quantity)

    def discount(self, orderitem):
        discount = 0 if not orderitem.product.discount else \
            orderitem.product.discount
        return discount

    def discount_price(self, orderitem):
        price = orderitem.product.price * orderitem.quantity
        discount = 0 if not orderitem.product.discount else \
            orderitem.product.discount
        discounted_price = price - (price * (discount/100))
        return round(discounted_price)


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.CartDetail)
