from rest_framework_nested import routers
from django.urls import path, include
from core.products.views import (
    ProductReadOnlyModelViewSet,
    ReviewModelViewSet,
    CollectionReadOnlyModelViewSet
)

# app_name = "core"

router = routers.DefaultRouter()
router.register("products", ProductReadOnlyModelViewSet)
router.register(
    "collections",
    CollectionReadOnlyModelViewSet
)

products_router = routers.NestedDefaultRouter(
    router,
    "products",
    lookup="product"
)
products_router.register(
    "reviews",
    ReviewModelViewSet,
    "product-reviews"
)


urlpatterns = [
    path('auth/', include("djoser.urls")),
    path('auth/', include("djoser.urls.jwt")),

    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
