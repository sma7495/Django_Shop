from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # Other URL patterns...
    path('add/post/', views.PostCreateView.as_view(), name="add_post"),
    path('edit/post/<int:pk>/', views.PostUpdateView.as_view(), name="edit_post"),
    path('list/post/', views.PostListView.as_view(), name="list_post"),
    path('delete/post/<int:pk>/', views.PostDeleteView.as_view(), name="delete_post"),    

    path('add/category/', views.CategoryCreateView.as_view(), name="add_category"),
    path('edit/category/<int:pk>/', views.CategoryUpdateView.as_view(), name="edit_category"),
    path('list/category/', views.CategoryListView.as_view(), name="list_category"),   
    path('delete/category/<int:pk>/', views.CategoryDeleteView.as_view(), name="delete_category"), 
    
    path('add/tag/', views.TagCreateView.as_view(), name="add_tag"),
    path('edit/tag/<int:pk>/', views.TagUpdateView.as_view(), name="edit_tag"),
    path('list/tag/', views.TagListView.as_view(), name="list_tag"), 
    path('delete/tag/<int:pk>/', views.TagDeleteView.as_view(), name="delete_tag"),    


]



urlpatterns += [
    path('api/categories/search/', views.category_search_api, name='category_search_api'),
    path('api/tags/search/', views.tag_search_api, name='tag_search_api'),
]