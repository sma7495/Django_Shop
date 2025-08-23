# your_app/templatetags/product_tags.py
import json
from django import template
from django.db.models import Count
from django.core.serializers import serialize
from ..models import ProductCategory, Product

register = template.Library()

@register.simple_tag(name = "get_category_data")
def get_category_data():
    # """
    # Returns category data for the chart
    # """
    # Use annotate to count products efficiently
    categories = ProductCategory.objects.annotate(
        product_count=Count('product')  # This counts products for each category
    ).values('title_fa', 'product_count')
    
    # Prepare data for the chart
    labels = [category['title_fa'] for category in categories]
    series = [category['product_count'] for category in categories]
    
    # labels = [1 , 2]
    # series = [3 , 8]
    return {
        'labels': labels,
        'series': series
    }


@register.simple_tag(name = "product_general_data")
def fun():
    return {
        'all' : Product.objects.all().count(),
        'draft_products': Product.objects.filter(status='draft').count(),
        'published_products': Product.objects.filter(status='published').count(),
        'low_stock_products': Product.objects.filter(stock__lte=50, stock__gt=0).count(),
        'high_stock_products': Product.objects.filter(stock__gt=50).count(),
        'out_of_stock_products': Product.objects.filter(stock=0).count(),
    }
    