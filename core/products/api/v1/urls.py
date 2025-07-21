from django.urls import path, include
from . import views

app_name = "products"

urlpatterns = [
    # Other URL patterns...
    path('list/', views.ProductListAPIView.as_view(), name='list'),
]