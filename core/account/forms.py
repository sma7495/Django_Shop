from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

from .models import Profile, Address

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    error_messages = {
        "invalid_login": _("رمز عبور یا نام کاربری صحیح نمی باشد"),
        "inactive": _("این حساب فعال نمی باشد"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
    # Email field (read-only)
    email = forms.EmailField(
        label='ایمیل',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'phone_number']
        
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'image': 'تصویر پروفایل',
            'phone_number': 'شماره تلفن',
        }
        
        help_texts = {
            'first_name': 'نام خود را وارد کنید',
            'last_name': 'نام خانوادگی خود را وارد کنید',
            'image': 'یک تصویر برای پروفایل خود انتخاب کنید',
            'phone_number': 'شماره تلفن باید 11 رقمی و با 09 شروع شود (مثال: 09123456789)',
        }
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09123456789'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial value for email field if instance exists
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        
        if phone_number:
            phone_number = phone_number.strip()
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            validator = RegexValidator(
                regex=r'^09\d{9}$',
                message='شماره تلفن باید 11 رقمی و با 09 شروع شود',
                code='invalid_phone'
            )
            try:
                validator(phone_number)
            except forms.ValidationError:
                raise forms.ValidationError('شماره تلفن باید 11 رقمی و با 09 شروع شود')
        
        return phone_number


class AddressForm(forms.ModelForm):
    """Form for creating and updating addresses with separate field definitions."""
    
    state = forms.CharField(
        label='استان',
        max_length=50,
        help_text='نام استان محل سکونت خود را وارد کنید',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: تهران',
            'dir': 'rtl',
        })
    )
    
    city = forms.CharField(
        label='شهر',
        max_length=50,
        help_text='نام شهر محل سکونت خود را وارد کنید',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: تهران',
            'dir': 'rtl',
        })
    )
    
    address = forms.CharField(
        label='آدرس کامل',
        help_text='آدرس کامل شامل خیابان، کوچه، پلاک و واحد را وارد کنید',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: خیابان آزادی، کوچه شهید فلانی، پلاک ۱۲',
            'rows': 4,
            'dir': 'rtl',
        })
    )
    
    zip_code = forms.CharField(
        label='کد پستی',
        max_length=10,
        help_text='کد پستی ۱۰ رقمی ایرانی را وارد کنید',
        validators=[Address.iran_zip_code_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: 1234567890',
            'maxlength': 10,
            'inputmode': 'numeric',
            'pattern': '\d{10}',
            'title': 'کد پستی باید ۱۰ رقم باشد',
        })
    )
    
    class Meta:
        model = Address
        fields = ['state', 'city', 'address', 'zip_code']
        error_messages = {
            'zip_code': {
                'invalid': 'کد پستی باید دقیقاً ۱۰ رقم باشد (فرمت ایرانی)'
            }
        }
    
    def clean_zip_code(self):
        """Additional validation for zip code"""
        zip_code = self.cleaned_data.get('zip_code')
        
        if zip_code:
            # Remove any non-digit characters
            zip_code = ''.join(filter(str.isdigit, zip_code))
            
            # Check if it's exactly 10 digits
            if len(zip_code) != 10:
                raise forms.ValidationError("کد پستی باید دقیقاً ۱۰ رقم باشد")
            
            # Optional: Validate Iranian zip code format
            # if not zip_code.startswith(('1', '2', '3')):  # Example validation
            #     raise forms.ValidationError("کد پستی معتبر نیست")
            
        return zip_code


class PersianChangePasswordForm(PasswordChangeForm):
    """
    A form for changing password with Persian labels and help text
    Includes old password field
    """
    old_password = forms.CharField(
        label=_("رمز عبور فعلی"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی را وارد کنید'
        }),
        help_text=_("برای تغییر رمز عبور، ابتدا رمز عبور فعلی خود را وارد کنید.")
    )
    
    new_password1 = forms.CharField(
        label=_("رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید'
        }),
        help_text=_(
            "رمز عبور شما نمی‌تواند شبیه سایر اطلاعات شخصی شما باشد.<br>"
            "رمز عبور شما باید حداقل شامل ۸ کاراکتر باشد.<br>"
            "رمز عبور شما نمی‌تواند یک رمز عبور متداول باشد.<br>"
            "رمز عبور شما نمی‌تواند کاملاً عددی باشد."
        )
    )
    
    new_password2 = forms.CharField(
        label=_("تکرار رمز عبور جدید"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را تکرار کنید'
        }),
        help_text=_("لطفاً رمز عبور جدید را مجدداً وارد کنید تا از صحت آن اطمینان حاصل شود.")
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Persian error messages
        self.error_messages = {
            'password_incorrect': _("رمز عبور فعلی وارد شده صحیح نمی‌باشد."),
            'password_mismatch': _("دو فیلد رمز عبور جدید مطابقت ندارند."),
            'password_too_short': _("رمز عبور بسیار کوتاه است. باید حداقل ۸ کاراکتر باشد."),
            'password_common': _("رمز عبور بسیار متداول است."),
            'password_entirely_numeric': _("رمز عبور نمی‌تواند کاملاً عددی باشد."),
        }

# contiue coiding ..................