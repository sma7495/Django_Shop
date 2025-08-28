from django.views.generic import TemplateView
from django.views.generic import DetailView
import requests
from django.views.generic import ListView
from django.db.models import Q, Case, When, IntegerField
from django.db.models.functions import Coalesce

from .models import Product
from .api.v1.serializers import ProductSerializer


class ProductListTemplateView(TemplateView):
    template_name = 'products/product_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Products'
        return context
  

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Serialize the product data
        serializer = ProductSerializer(product, context={'request': self.request})
        context['product_data'] = serializer.data
        
        #Add any additional context you might need
        context['related_products'] = Product.objects.filter(
            category__in=product.category.all()
        ).exclude(id=product.id).distinct()[:4]
        
        return context  
    


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20  # Matches your HTML which shows 20 products per page
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='published')
        
        # Get sorting parameter
        sort = self.request.GET.get('sort', 'newest')
        
        # Apply sorting
        if sort == 'popular':
            # You might need to add a view_count field to your model for this
            # queryset = queryset.order_by('-view_count')
            pass
        elif sort == 'newest':
            queryset = queryset.order_by('-created_date')
        elif sort == 'bestselling':
            # You might need to add a sold_count field to your model for this
            # queryset = queryset.order_by('-sold_count')
            pass
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-created_date')
            
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title_en__icontains=search_query) |
                Q(title_fa__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(brief_description__icontains=search_query)
            )
            
        return queryset.select_related('guarantee').prefetch_related('color', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'newest')
        return context


# continue coideing ..............