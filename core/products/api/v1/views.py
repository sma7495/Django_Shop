from rest_framework.generics import ListAPIView

from .paginators import ProductPagination
from .serializers import ProductSerializer
from ...models import Product


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination