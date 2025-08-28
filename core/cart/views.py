from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse


from .cart import CartSession
from products.models import Product

# Create your views here.
class SessionAddProductView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if Product.objects.filter(id = int(product_id), status = "published", stock__gt =0):
            cart.add_product(product_id)
        return JsonResponse({"cart": cart.get_dict(), "total_quantity": cart.get_total_quantity()})

class SessionUpdateProductQuantityView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        cart.update_item_quantity(request.POST.get("product_id") , request.POST.get("quantity"))
        return JsonResponse({"cart": cart.get_dict(), "total_quantity": cart.get_total_quantity()})