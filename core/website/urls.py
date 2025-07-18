from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    # path('services/', views.ServicesPageView.as_view(), name='services'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    # path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('faq/', views.FAQPageView.as_view(), name='faq'),
]