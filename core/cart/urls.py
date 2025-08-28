from django.urls import path,re_path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add_product/",views.SessionAddProductView.as_view(),name="session_add_product"),
    path("", views.SessionUpdateProductQuantityView.as_view(), name = "session_update_product_quantity"),
    # path("session/remove-product/",views.SessionRemoveProductView.as_view(),name="session-remove-product"),
    # path("session/update-product-quantity/",views.SessionUpdateProductQuantityView.as_view(),name="session-update-product-quantity"),
    # path("summary/",views.CartSummaryView.as_view(),name="cart-summary")
]

