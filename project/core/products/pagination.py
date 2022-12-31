from rest_framework.pagination import PageNumberPagination


class CollectionPagination(PageNumberPagination):
    page_size = 1
