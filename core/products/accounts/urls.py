from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # Other URL patterns...
    path("add/product/", views.ProductCreateView.as_view(), name="add_product"),
    path("edit/product/<int:pk>", views.ProductUpdateView.as_view(), name="edit_product"),
    path("list/product/", views.ProductListView.as_view(), name="list_product"),
    
    path("add/product/category/", views.ProductCategoryCreateView.as_view(), name="add_category"),
    path("edit/product/category/<int:pk>", views.ProductCategoryUpdateView.as_view(), name="edit_category"),
    path("list/product/category/", views.ProductCategoryListView.as_view(), name="list_category"),

    path("add/product/guarantee/", views.ProductguaranteeCreateView.as_view(), name="add_guarantee"),
    path("edit/product/guarantee/<int:pk>", views.ProductguaranteeUpdateView.as_view(), name="edit_guarantee"),
    path("list/product/guarantee/", views.ProductguaranteeListView.as_view(), name="list_guarantee"),
    
    path("add/product/color/", views.ProductColorCreateView.as_view(), name="add_color"),
    path("edit/product/color/<int:pk>", views.ProductColorUpdateView.as_view(), name="edit_color"),
    path("list/product/color/", views.ProductColorListView.as_view(), name="list_color"),
    
    path("add/product/video/", views.ProductVideoCreateView.as_view(), name="add_video"),
    path("edit/product/video/<int:pk>", views.ProductVideoUpdateView.as_view(), name="edit_video"),
    path("list/product/video/", views.ProductVideoListView.as_view(), name="list_video"),

]

urlpatterns += [
    path('api/products/search/', views.product_search_api, name='product_search_api'),
    path('api/categories/search/', views.category_search_api, name='category_search_api'),
    path('api/colors/search/', views.color_search_api, name='color_search_api'),
    path('api/guarantees/search/', views.guarantee_search_api, name='guarantee_search_api'),
]