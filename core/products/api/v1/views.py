from rest_framework.generics import ListAPIView
from rest_framework import filters

from .paginators import ProductPagination
from .serializers import ProductSerializer
from ...models import Product


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(status = 'published')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.OrderingFilter]  # Enable ordering
    ordering_fields = ['price', 'created_date', 'discount_percent']  # Allowable fields
    ordering = ['-created_date']  # Default ordering (newest first)
    