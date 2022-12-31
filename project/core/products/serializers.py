from django.conf import settings
from rest_framework import serializers
from .models import (
    Product,
    Variation,
    Image,
    Review,
    Collection
)


class VariationSerializer(serializers.ModelSerializer):
    key = serializers.StringRelatedField()
    value = serializers.StringRelatedField()

    class Meta:
        model = Variation
        fields = ["key", "value"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    collection_url = serializers.HyperlinkedRelatedField(
        view_name="collection-detail",
        read_only=True,
        source="collection"
    )
    currency = serializers.SerializerMethodField(method_name="get_currency")
    variations = VariationSerializer(many=True)
    images = ImageSerializer(many=True)
    collection = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "collection",
            "collection_url",
            "title",
            "price",
            "discount",
            "unit",
            "currency",
            "description",
            "variations",
            "images",
            "delivery_time_in_days"
        ]

    def get_currency(self, obj):
        return settings.CURRENCY


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    editing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "description",
            "rating",
            "editing"
        ]

    def create(self, validated_data):
        if Review.objects.filter(
            product_id=self.context["product_id"],
            user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError(
                "Only one review can be posted for one product."
            )

        return Review.objects.create(
            product_id=self.context["product_id"],
            user=self.context["request"].user,
            **validated_data
        )

    def update(self, instance: Review, validated_data):
        try:
            product_id = int(self.context["product_id"])
            user = self.context["request"].user
        except:
            raise serializers.ValidationError("Invalid Request")

        if instance.user != user or instance.product.id != product_id:
            raise serializers.ValidationError(
                "Invalid Request"
            )

        instance.description = validated_data.get("description")
        instance.rating = validated_data.get("rating")
        instance.save()
        return instance


class CollectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)
    products_count = serializers.SerializerMethodField(
        method_name="get_products_count"
    )

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count", "products"]

    def get_products_count(self, instance: Collection):
        return instance.products.all().count()
