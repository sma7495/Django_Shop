from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomAuthenticationForm  # You'll need to create this

class PersianLoginRequiredMixin(LoginRequiredMixin):
    """Custom LoginRequiredMixin with Persian messages."""
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "برای دسترسی به این صفحه باید وارد حساب کاربری خود شوید."  # "You must be logged in to access this page."
        )
        return super().handle_no_permission()



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login_signup.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        email = form.cleaned_data.get('username')  # Because email is USERNAME_FIELD
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(self.request, user)
                # Add success message
                messages.success(
                    self.request,
                    f"خوش آمدید."
                )
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error(None, "این حساب کاربری فعال نیست.")
                return self.form_invalid(form)
        else:
            form.add_error(None, "ایمیل یا رمز عبور نامعتبر است.")
            return self.form_invalid(form)
    
    


class CustomLogoutView(PersianLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "شما با موفقیت از حساب کاربری خود خارج شدید.")
        return redirect('account:login')  # Redirect to your login page
    

# continue coding..........................