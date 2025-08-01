from django.urls import path, include
from . import views

app_name = "api"

urlpatterns = [
    # Other URL patterns...
    path('list/', views.ProductListAPIView.as_view(), name='list'),
    path('create/', views.ProductCreateAPIView.as_view(), name='create'),
    path('delete/<int:pk>/', views.ProductDeleteAPIView.as_view(), name='delete'),
    path('update/<int:pk>/', views.ProductPartialUpdateAPIView.as_view(), name='update'),
    path('detail/<int:pk>/', views.ProductDetailAPIView.as_view(), name='detail'),
]