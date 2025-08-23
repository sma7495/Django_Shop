from django.urls import path, include

from . import views

app_name = "admin"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    
]
