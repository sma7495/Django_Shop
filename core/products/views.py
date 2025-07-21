from django.views.generic import TemplateView
from .models import Product


class ProductListTemplateView(TemplateView):
    template_name = 'product/product_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Products'
        return context