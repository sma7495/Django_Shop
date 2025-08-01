from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .paginators import ProductPagination
from .serializers import ProductSerializer
from ...models import Product
from .permissions import IsAdminOrSuperUser, IsProductOwnerOrAdmin


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(status = 'published')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.OrderingFilter]  # Enable ordering
    ordering_fields = ['price', 'created_date', 'discount_percent']  # Allowable fields
    ordering = ['-created_date']  # Default ordering (newest first)
    

class ProductCreateAPIView(CreateAPIView):
    """
    API endpoint that allows products to be created.
    Requires authentication.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSuperUser]  # Only authenticated users can create products

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
      # Automatically set the user to the current authenticated user
        data = request.data.copy()  # Create a mutable copy
        data["user"] = request.user.id  # Now you can modify it
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Call perform_create to save with the user
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        

class ProductDeleteAPIView(DestroyAPIView):
    """
    API endpoint that allows admin users to delete products.
    """
    queryset = Product.objects.all()
    permission_classes = [IsProductOwnerOrAdmin]
    lookup_field = 'pk'  # Default is 'pk', but explicit is better

    def perform_destroy(self, instance):
        """
        Perform the actual deletion.
        Can add pre-deletion logic here if needed.
        """
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """
        Custom response for deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class ProductPartialUpdateAPIView(UpdateAPIView):
    """
    API endpoint that allows product owners or admins to partially update products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductOwnerOrAdmin]
    lookup_field = 'pk'
    
    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_update(self, serializer):
        # For admins: allow changing user
        # For owners: keep the original user
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            serializer.validated_data.pop('user', None)
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            'detail': 'Product partially updated successfully.',
            'product': response.data
        }, status=status.HTTP_200_OK)


class ProductDetailAPIView(RetrieveAPIView):
    """
    API endpoint for retrieving detailed product information.
    Public read access, but requires owner/admin for write operations.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]  # Public read access

    def get_permissions(self):
        """
        Dynamically assign permissions based on request method:
        - Safe methods (GET, HEAD, OPTIONS): AllowAny
        - Write methods (PUT, PATCH, DELETE): IsAuthenticated + IsProductOwnerOrAdmin
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsProductOwnerOrAdmin()]

    def retrieve(self, request, *args, **kwargs):
        """Enhanced retrieve with view count increment"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Increment view count if this is a GET request from non-owner
        # if request.method == 'GET' and instance.user != request.user:
        #     instance.view_count = models.F('view_count') + 1
        #     instance.save(update_fields=['view_count'])
        
        return Response(serializer.data)

        # Optional: Include update/delete methods in the same view
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)


# continue coding.............
    