from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class AdminOrSuperuserRequiredMixin:
    """Verify that the current user is admin or superuser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.type in [2, 3] or request.user.is_superuser):
            raise PermissionDenied("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)
    

class PersianLoginRequiredMixin(LoginRequiredMixin):
    """Custom LoginRequiredMixin with Persian messages."""
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "برای دسترسی به این صفحه باید وارد حساب کاربری خود شوید."  # "You must be logged in to access this page."
        )
        return super().handle_no_permission()