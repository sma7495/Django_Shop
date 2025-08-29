from django.core.exceptions import PermissionDenied

class AdminOrSuperuserRequiredMixin:
    """Verify that the current user is admin or superuser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.type in [2, 3] or request.user.is_superuser):
            raise PermissionDenied("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)