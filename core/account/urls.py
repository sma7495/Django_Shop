from django.urls import path, include

from . import views

app_name = "account"

urlpatterns = [
    path("api/v1/", include("account.api.v1.urls")),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/",views.CustomLoginView.as_view(), name= "login"),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
