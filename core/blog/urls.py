from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    # Other URL patterns...
    path('accounts/', include("blog.accounts.urls")),

]
