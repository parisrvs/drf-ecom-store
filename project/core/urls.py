from rest_framework_nested import routers
from django.urls import path, include
from core.products.views import ProductReadOnlyModelViewSet, ReviewModelViewSet

app_name = "core"

router = routers.DefaultRouter()
router.register("products", ProductReadOnlyModelViewSet)

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
    path('', include(router.urls)),
    path('', include(products_router.urls))
]
