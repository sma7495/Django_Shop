# your_app/templatetags/product_tags.py
import json
from django import template
from django.db.models import Count
from django.core.serializers import serialize

from products.models import Product
register = template.Library()

@register.simple_tag(name = "get_product_data")
def fun(id):
    return Product.objects.get(id=id)


@register.simple_tag(name = "get_total_price")
def fun(price, quantity):
    return int(price) * int(quantity)

