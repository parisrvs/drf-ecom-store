from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from core.products import models


class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["title"]
    }
    list_display = ["title", "product_count"]
    search_fields = ["title__istartswith"]
    list_per_page = 10

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        url = reverse("admin:products_product_changelist") + '?' + urlencode({
            "collection__id": str(collection.id)
        })
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            collection.product_count
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count("products")
        )


class DiscountAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "percent"]
    search_fields = ["code__istartswith"]
    list_per_page = 10
    list_editable = ["code", "percent"]


class KeyAdmin(admin.ModelAdmin):
    list_display = ["id", "key", "values_count"]
    search_fields = ["key__istartswith"]
    list_editable = ["key"]
    list_per_page = 20
    list_select_related = True

    @admin.display(ordering="values_count")
    def values_count(self, key):
        url = reverse("admin:products_value_changelist") + '?' + urlencode({
            "key__id": key.id
        })
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            key.values_count
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            values_count=Count("values")
        )


class ValueAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]
    search_fields = ["value__istartswith"]
    list_editable = ["value"]
    list_per_page = 20


class PincodeAdmin(admin.ModelAdmin):
    list_display = [
        "pincode", "delivery_time_in_days",
        "count_of_products_not_available"
    ]
    list_per_page = 10
    filter_horizontal = ["products_not_available"]
    search_fields = ["pincode__istartswith"]
    list_editable = ["delivery_time_in_days"]

    @admin.display(ordering="count_of_products_not_available")
    def count_of_products_not_available(self, pincode):
        return pincode.count_of_products_not_available

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count_of_products_not_available=Count("products_not_available")
        )


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["title"]
    }
    list_display = [
        "id",
        "title",
        "price",
        "discount",
        "discount_price",
        "unit",
        "availability",
        "inventory",
        "delivery_time_in_days",
        "created_at"
    ]
    list_per_page = 10
    list_select_related = ["collection"]
    list_editable = [
        "inventory", "price",
        "availability", "delivery_time_in_days",
        "discount"
    ]
    filter_horizontal = ["images", "variations", "tags"]
    autocomplete_fields = ["collection"]
    search_fields = ["title__istartswith"]

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "variations":
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            kwargs["queryset"] = qs.select_related("key", "value")
        return super().formfield_for_manytomany(
            db_field,
            request=request,
            **kwargs
        )

    def discount_price(self, product):
        if not product.discount:
            return product.price
        return round(
            product.price - (product.price * (product.discount / 100))
        )


class RatingFilter(admin.SimpleListFilter):
    title = "Rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ('1', "1 Star"),
            ('2', "2 Star"),
            ('3', "3 Star"),
            ('4', "4 Star"),
            ('5', "5 Star"),
        ]

    def queryset(self, request, queryset):
        if self.value() in ['1', '2', '3', '4', '5']:
            rating = int(self.value())
            return queryset.filter(rating=rating)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user", "product", "rating"]
    list_per_page = 10
    autocomplete_fields = ["user", "product"]
    list_filter = [RatingFilter]


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["tag"]
    }
    list_display = ["id", "tag", "count_of_products"]
    search_fields = ["tag__istartswith"]
    list_per_page = 10
    list_editable = ["tag"]

    @admin.display(ordering="count_of_products")
    def count_of_products(self, tag):
        url = reverse("admin:products_product_changelist") + '?' + urlencode({
            "tags__id": str(tag.id)
        })
        return format_html(
            "<a href='{}'>{}</a>",
            url,
            tag.count_of_products
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count_of_products=Count("products")
        )


class VariationAdmin(admin.ModelAdmin):
    list_display = ["id", "key", "value"]
    list_per_page = 10
    autocomplete_fields = ["key", "value"]
    list_select_related = ["key", "value"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "thumbnail"]
    readonly_fields = ["Display"]
    list_editable = ["name"]

    def thumbnail(self, instance):
        return format_html(
            f"<img src={instance.image.url} class='thumbnail' />"
        )

    def Display(self, instance):
        return format_html(
            f"<img src={instance.image.url} />"
        )

    class Media:
        css = {
            "all": ["products/styles.css"]
        }


admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Key, KeyAdmin)
admin.site.register(models.Value, ValueAdmin)
admin.site.register(models.Variation, VariationAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Pincode, PincodeAdmin)
