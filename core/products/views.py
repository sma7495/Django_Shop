from django.views.generic import TemplateView
from django.views.generic import DetailView
import requests

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
    
# continue coideing ..............