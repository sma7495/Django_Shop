from django.urls import path, include
from . import views

app_name = "products"

urlpatterns = [
    # Other URL patterns...
    path('api/v1/', include("products.api.v1.urls")),
    path('accounts/', include("products.accounts.urls")),
    path('list/', views.ProductListTemplateView.as_view(), name='list'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='detail'),
]