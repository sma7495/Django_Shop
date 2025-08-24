from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView 
from django.urls import reverse_lazy
from django.contrib import messages


from ..models import Profile
from ..forms import ProfileForm
from .mixins import PersianLoginRequiredMixin, AdminOrSuperuserRequiredMixin

class HomeView(PersianLoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    """Home view that requires login"""
    template_name = 'accounts/admin/home.html'  # specify your template path
    
    # Optional: You can add context data if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here
        context['user'] = self.request.user
        return context

