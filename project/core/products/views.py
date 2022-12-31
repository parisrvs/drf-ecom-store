from itertools import chain

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

from .models import Product, Review, Collection
from .serializers import ProductSerializer, ReviewSerializer, CollectionSerializer
from .pagination import CollectionPagination

from django.db.models import Value as V


class ProductReadOnlyModelViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related(
        "collection"
    ).prefetch_related(
        "variations__key",
        "variations__value",
        "images"
    ).all()

    def get_serializer_context(self):
        return {"request": self.request}


class ReviewModelViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch"]
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        current_user = self.request.user.is_authenticated
        current_user_review = Review.objects.filter(
            product_id=self.kwargs["product_pk"],
            user=self.request.user
        ).exists()

        """
        This if condition ensures that if a,
        user is authenticated and has posted a review,
        then that review comes at the top of the review list.
        """
        if current_user and current_user_review:
            queryset = Review.objects.filter(
                product_id=self.kwargs["product_pk"]
            ).exclude(
                user=self.request.user
            ).select_related(
                "product",
                "user"
            ).annotate(
                editing=V(False)
            )

            review = Review.objects.filter(
                product_id=self.kwargs["product_pk"],
                user=self.request.user
            ).select_related(
                "product",
                "user"
            ).annotate(
                editing=V(True)
            )

            return list(chain(review, queryset))

        return Review.objects.filter(
            product_id=self.kwargs["product_pk"]
        ).select_related(
            "product",
            "user"
        ).annotate(
            editing=V(False)
        )

    def get_serializer_context(self):
        return {"request": self.request, "product_id": self.kwargs["product_pk"]}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return super().destroy(request, *args, **kwargs)


class CollectionReadOnlyModelViewSet(ReadOnlyModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all().prefetch_related(
        "products",
        "products__variations__key",
        "products__variations__value",
        "products__images"
    )
    pagination_class = CollectionPagination
