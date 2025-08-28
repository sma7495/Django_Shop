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
from django.views.generic import TemplateView, UpdateView
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext_lazy as _


from .models import Profile, Address
from .forms import ProfileForm, AddressForm, PersianChangePasswordForm, CustomAuthenticationForm

User = get_user_model()

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
    template_name = 'accounts/signin.html'
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
        
    def get_success_url(self):
        """
        Redirect users based on their type
        Assuming user type is stored in user.user_type or similar field
        """
        # Get the logged-in user
        user = self.request.user
        
        # Check user type and redirect accordingly
        if hasattr(user, 'type'):
            if user.type == 2 or user.type == 3:
                # Redirect for user type = admin or superuser
                return reverse_lazy("account:admin_app:home")
            elif user.type == 3:
                # Redirect for user type = customer
                return reverse_lazy("website:home")  # Change this to your desired URL
        
        # Default redirect if user type doesn't match or isn't set
        return reverse_lazy("website:home")   # Change this to your default URL
    

class CustomLogoutView(PersianLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "شما با موفقیت از حساب کاربری خود خارج شدید.")
        return redirect('account:login')  # Redirect to your login page


class ProfileUpdateView(PersianLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')
    
    # Define template mapping
    template_mapping = {
        'admin': 'accounts/admin/profile.html',
        'customer': 'accounts/customer/profile.html'
    }
    
    def get_template_names(self):
        """
        Select template based on user type using mapping
        """
        if self.request.user.type == 2 or self.request.user.type == 3:
            return self.template_mapping['admin']
        else:
            return self.template_mapping['customer']
    
    def get_object(self, queryset=None):
        """
        Return the profile object for the current user
        """
        try:
            return Profile.objects.get(id=self.request.user.id)
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """
        Add extra context to the template including address formset
        """
        context = super().get_context_data(**kwargs)
        
        # Create formset for addresses
        AddressFormSet = inlineformset_factory(
            Profile, 
            Address, 
            form=AddressForm,  # You'll need to create an AddressForm
            extra=1, 
            can_delete=True,
            max_num=5  # Limit to 5 addresses maximum
        )
        
        if self.request.POST:
            context['address_formset'] = AddressFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['address_formset'] = AddressFormSet(instance=self.object)
        
        context['title'] = 'ویرایش پروفایل'
        return context
    
    def form_valid(self, form):
        """
        Handle successful form submission for both profile and addresses
        """
        context = self.get_context_data()
        address_formset = context['address_formset']
        # Check if both profile form and address formset are valid
        if address_formset:
            if address_formset.is_valid():
                # Save profile first
                self.object = form.save()
                
                # Save addresses
                addresses = address_formset.save(commit=False)
                for address in addresses:
                    address.profile = self.object
                    address.save()
                
                # Delete any marked addresses
                for obj in address_formset.deleted_objects:
                    obj.delete()
                    
                messages.success(self.request, 'پروفایل و آدرس‌ها با موفقیت به‌روزرسانی شد')
                return redirect(self.get_success_url())
            else:
                # If address formset is invalid, show errors
                messages.error(self.request, 'لطفاً خطاهای مربوط به آدرس‌ها را اصلاح کنید')
                return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        """
        Handle invalid form submission
        """
        messages.error(self.request, 'لطفاً خطاهای زیر را اصلاح کنید')
        return super().form_invalid(form)



class PersianPasswordChangeView(PersianLoginRequiredMixin, PasswordChangeView):
    """
    View for changing password with Persian interface
    Includes old password field and Lobibox success message
    """
    form_class = PersianChangePasswordForm
    success_url = reverse_lazy('account:password_change')  # Redirect to same page

    # Define template mapping
    template_mapping = {
        'admin': 'accounts/admin/change_password.html',
        'customer': 'accounts/customer/change_password.html'
    }
    
    def get_template_names(self):
        """
        Select template based on user type using mapping
        """
        if self.request.user.type == 2 or self.request.user.type == 3:
            return self.template_mapping['admin']
        else:
            return self.template_mapping['customer']

    def form_valid(self, form):
        # Save the form and set success message
        response = super().form_valid(form)
        messages.success(self.request, _("رمز عبور شما با موفقیت تغییر یافت."))
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("تغییر رمز عبور")
        context['submit_label'] = _("ذخیره تغییرات")
        context['cancel_url'] = reverse_lazy('account:login')  # Adjust to your profile URL
        return context
    
# continue coding..........................