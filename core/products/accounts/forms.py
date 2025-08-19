from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import uuid
import os
from django.contrib.auth import get_user_model
from django.utils.text import slugify
        
from ..models import Product, ProductImage, ProductCategory, ProductGuarantee, ProductColor, ProductVideos

User = get_user_model()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'user',
            'title_en',
            'title_fa',
            'slug',
            'image',
            'color',
            'guarantee',
            'description',
            'brief_description',
            'stock',
            'price',
            'discount_percent',
            'status',
            'category',
        ]
        labels = {
            'user': 'کاربر',
            'title_en': 'عنوان انگلیسی',
            'title_fa': 'عنوان فارسی',
            'slug': 'نامک (Slug)',
            'image': 'تصویر محصول',
            'color': 'رنگ‌های موجود',
            'guarantee': 'گارانتی',
            'description': 'توضیحات کامل',
            'brief_description': 'توضیحات مختصر',
            'stock': 'موجودی انبار',
            'price': 'قیمت (تومان)',
            'discount_percent': 'درصد تخفیف',
            'status': 'وضعیت انتشار',
            'category': 'دسته‌بندی‌ها',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'brief_description': forms.Textarea(attrs={'rows': 2}),
            'color': forms.SelectMultiple(attrs={'class': 'select2'}),
            'category': forms.SelectMultiple(attrs={'class': 'select2'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'slug': 'در صورت خالی گذاشتن، به صورت خودکار از عنوان انگلیسی تولید می‌شود',
            'discount_percent': 'عدد بین ۰ تا ۱۰۰',
            'title_en': 'لطفاً فقط از حروف انگلیسی استفاده کنید',
            'title_fa': 'لطفاً فقط از حروف فارسی استفاده کنید',
            'image': 'تصویر اصلی محصول را انتخاب کنید',
            'color': 'می‌توانید چند رنگ انتخاب کنید',
            'guarantee': 'گارانتی محصول را انتخاب کنید',
            'description': 'توضیحات کامل محصول به همراه تمام جزئیات',
            'brief_description': 'توضیحات کوتاه برای نمایش در کارت محصول',
            'stock': 'تعداد موجودی در انبار',
            'price': 'قیمت محصول به ریال',
            'status': 'وضعیت نمایش محصول را انتخاب کنید',
            'category': 'می‌توانید چند دسته‌بندی انتخاب کنید',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom initialization
        self.fields['guarantee'].required = False
        self.fields['color'].required = False
        
        # Add custom CSS classes to fields
        for field in self.fields:
            if field not in ['color', 'category', 'status']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            # Auto-generate slug if not provided
            title_en = self.cleaned_data.get('title_en', '')
            if title_en:
                slug = slugify(title_en) + '-' + str(uuid.uuid4())[:8]
            else:
                raise ValidationError("عدم امکان تولید خودکار نامک - عنوان انگلیسی الزامی است")
        return slug

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError("قیمت باید عددی مثبت باشد")
        return price

    def clean_discount_percent(self):
        discount_percent = self.cleaned_data.get('discount_percent')
        if discount_percent is not None and discount_percent > 100:
            raise ValidationError("درصد تخفیف نمی‌تواند بیشتر از ۱۰۰ باشد")
        return discount_percent

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise ValidationError("موجودی نمی‌تواند منفی باشد")
        return stock

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']
        labels = {
            'product': 'محصول',
            'image': 'تصویر محصول',
        }
        help_texts = {
            'product': 'محصولی که این تصویر به آن تعلق دارد را انتخاب کنید',
            'image': 'تصویری با کیفیت بالا از محصول انتخاب کنید (فرمت‌های JPEG, PNG, WEBP پشتیبانی می‌شوند)',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the product queryset here if needed
        # self.fields['product'].queryset = Product.objects.filter(...)
        
        # Add required class to labels for required fields
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError("لطفاً یک تصویر انتخاب کنید")
            
        # Validate image size (example: max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if image.size > max_size:
            raise ValidationError("حجم تصویر نباید بیشتر از ۵ مگابایت باشد")
            
        # Validate file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        extension = os.path.splitext(image.name)[1].lower()
        if extension not in valid_extensions:
            raise ValidationError("فرمت فایل نامعتبر است. فقط فرمت‌های JPEG, PNG, WEBP قابل قبول هستند")
            
        return image

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validation here if needed
        return cleaned_data

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['title_en', 'title_fa', 'slug']
        
        labels = {
            'title_en': 'عنوان انگلیسی',
            'title_fa': 'عنوان فارسی',
            'slug': 'اسلاگ',
        }
        
        help_texts = {
            'title_en': 'لطفاً عنوان را به انگلیسی وارد نمایید (فقط حروف انگلیسی مجاز است)',
            'title_fa': 'لطفاً عنوان را به فارسی وارد نمایید (فقط حروف فارسی مجاز است)',
            'slug': 'یک شناسه منحصر به فرد برای URL. اگر خالی باشد به طور خودکار از عنوان انگلیسی ایجاد می‌شود',
        }
        
        error_messages = {
            'title_en': {
                'required': 'وارد کردن عنوان انگلیسی الزامی است',
                'invalid': 'عنوان انگلیسی وارد شده معتبر نیست',
            },
            'title_fa': {
                'required': 'وارد کردن عنوان فارسی الزامی است',
                'invalid': 'عنوان فارسی وارد شده معتبر نیست',
            },
            'slug': {
                'required': 'وارد کردن اسلاگ الزامی است',
                'invalid': 'اسلاگ وارد شده معتبر نیست',
                'unique': 'این اسلاگ قبلاً استفاده شده است',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add additional attributes to fields here if needed
        self.fields['title_en'].widget.attrs.update({'class': 'form-control', 'placeholder': 'English title'})
        self.fields['title_fa'].widget.attrs.update({'class': 'form-control', 'placeholder': 'عنوان فارسی'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control', 'placeholder': 'اسلاگ'})
        
    def clean(self):
        cleaned_data = super().clean()
        title_en = cleaned_data.get('title_en')
        slug = cleaned_data.get('slug')
        
        # Auto-generate slug if empty and title_en exists
        if title_en and not slug:
            cleaned_data['slug'] = self.generate_slug(title_en)
            # Update the form's slug field value
            self.initial['slug'] = cleaned_data['slug']
            
        return cleaned_data

    def generate_slug(self, title):
        """
        Generate a URL-friendly slug from the English title
        """
        # First slugify the title
        slug = slugify(title)
            
        return slug

class ProductGuaranteeForm(forms.ModelForm):
    class Meta:
        model = ProductGuarantee
        fields = ['title_en', 'title_fa', 'slug', 'description']
        
        labels = {
            'title_en': 'عنوان انگلیسی',
            'title_fa': 'عنوان فارسی',
            'slug': 'اسلاگ',
            'description': 'توضیحات',
        }
        
        help_texts = {
            'title_en': 'لطفاً عنوان گارانتی را به انگلیسی وارد نمایید (فقط حروف انگلیسی مجاز است)',
            'title_fa': 'لطفاً عنوان گارانتی را به فارسی وارد نمایید (فقط حروف فارسی مجاز است)',
            'slug': 'یک شناسه منحصر به فرد برای URL. اگر خالی باشد به طور خودکار از عنوان انگلیسی ایجاد می‌شود',
            'description': 'توضیحات اختیاری درباره شرایط گارانتی (می‌تواند خالی باشد)',
        }
        
        error_messages = {
            'title_en': {
                'required': 'وارد کردن عنوان انگلیسی الزامی است',
                'invalid': 'عنوان انگلیسی وارد شده معتبر نیست',
                'max_length': 'عنوان انگلیسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'title_fa': {
                'required': 'وارد کردن عنوان فارسی الزامی است',
                'invalid': 'عنوان فارسی وارد شده معتبر نیست',
                'max_length': 'عنوان فارسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'slug': {
                'required': 'وارد کردن اسلاگ الزامی است',
                'invalid': 'اسلاگ وارد شده معتبر نیست',
                'unique': 'این اسلاگ قبلاً استفاده شده است',
                'max_length': 'اسلاگ نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and placeholders to form fields
        self.fields['title_en'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'English guarantee title'
        })
        self.fields['title_fa'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'عنوان گارانتی به فارسی'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'اسلاگ گارانتی'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'توضیحات درباره گارانتی...',
            'rows': 4
        })
        
    def clean(self):
        cleaned_data = super().clean()
        title_en = cleaned_data.get('title_en')
        slug = cleaned_data.get('slug')
        
        # Auto-generate slug if empty and title_en exists
        if title_en and not slug:
            cleaned_data['slug'] = self.generate_slug(title_en)
            # Update the form's slug field value
            self.initial['slug'] = cleaned_data['slug']
            
        return cleaned_data

    def generate_slug(self, title):
        """
        Generate a URL-friendly slug from the English title
        """
        # First slugify the title
        slug = slugify(title)
            
        return slug
    
class ProductColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ['title_en', 'title_fa', 'slug']
        
        labels = {
            'title_en': 'عنوان انگلیسی',
            'title_fa': 'عنوان فارسی',
            'slug': 'اسلاگ',
        }
        
        help_texts = {
            'title_en': 'لطفاً نام رنگ را به انگلیسی وارد نمایید (فقط حروف انگلیسی مجاز است)',
            'title_fa': 'لطفاً نام رنگ را به فارسی وارد نمایید (فقط حروف فارسی مجاز است)',
            'slug': 'شناسه یکتا برای URL. در صورت خالی بودن، از عنوان انگلیسی به صورت خودکار ایجاد می‌شود',
        }
        
        error_messages = {
            'title_en': {
                'required': 'وارد کردن عنوان انگلیسی الزامی است',
                'invalid': 'عنوان انگلیسی وارد شده معتبر نیست',
                'max_length': 'عنوان انگلیسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'title_fa': {
                'required': 'وارد کردن عنوان فارسی الزامی است',
                'invalid': 'عنوان فارسی وارد شده معتبر نیست',
                'max_length': 'عنوان فارسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'slug': {
                'required': 'وارد کردن اسلاگ الزامی است',
                'invalid': 'اسلاگ وارد شده معتبر نیست',
                'unique': 'این اسلاگ قبلاً استفاده شده است',
                'max_length': 'اسلاگ نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and placeholders to form fields
        self.fields['title_en'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Color name in English'
        })
        self.fields['title_fa'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'نام رنگ به فارسی'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'اسلاگ رنگ'
        })

    def clean(self):
        cleaned_data = super().clean()
        title_en = cleaned_data.get('title_en')
        slug = cleaned_data.get('slug')
        
        # Auto-generate slug if empty and title_en exists
        if title_en and not slug:
            cleaned_data['slug'] = self.generate_slug(title_en)
            # Update the form's slug field value
            self.initial['slug'] = cleaned_data['slug']
            
        return cleaned_data

    def generate_slug(self, title):
        """
        Generate a URL-friendly slug from the English title
        """
        # First slugify the title
        slug = slugify(title)
            
        return slug

class ProductVideosForm(forms.ModelForm):
    class Meta:
        model = ProductVideos
        fields = ['user', 'product', 'title_en', 'title_fa', 'slug', 'cover', 'video_url', 'description']
        
        labels = {
            'user': 'کاربر',
            'product': 'محصولات مرتبط',
            'title_en': 'عنوان انگلیسی',
            'title_fa': 'عنوان فارسی',
            'slug': 'اسلاگ',
            'cover': 'کاور ویدیو',
            'video_url': 'لینک ویدیو',
            'description': 'توضیحات',
        }
        
        help_texts = {
            'user': 'کاربری که این ویدیو را ایجاد کرده است',
            'product': 'محصولاتی که این ویدیو به آنها مرتبط است (می‌توانید چندین محصول انتخاب کنید)',
            'title_en': 'لطفاً عنوان ویدیو را به انگلیسی وارد نمایید (فقط حروف انگلیسی مجاز است)',
            'title_fa': 'لطفاً عنوان ویدیو را به فارسی وارد نمایید (فقط حروف فارسی مجاز است)',
            'slug': 'شناسه یکتا برای URL. در صورت خالی بودن، از عنوان انگلیسی به صورت خودکار ایجاد می‌شود',
            'cover': 'تصویر کاور ویدیو (ترجیحاً با ابعاد 16:9)',
            'video_url': 'لینک ویدیو در پلتفرم‌های میزبانی ویدیو مانند یوتیوب، آپارات و...',
            'description': 'توضیحات اختیاری درباره ویدیو (می‌تواند خالی باشد)',
        }
        
        error_messages = {
            'user': {
                'required': 'انتخاب کاربر الزامی است',
            },
            'title_en': {
                'required': 'وارد کردن عنوان انگلیسی الزامی است',
                'invalid': 'عنوان انگلیسی وارد شده معتبر نیست',
                'max_length': 'عنوان انگلیسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'title_fa': {
                'required': 'وارد کردن عنوان فارسی الزامی است',
                'invalid': 'عنوان فارسی وارد شده معتبر نیست',
                'max_length': 'عنوان فارسی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'slug': {
                'required': 'وارد کردن اسلاگ الزامی است',
                'invalid': 'اسلاگ وارد شده معتبر نیست',
                'unique': 'این اسلاگ قبلاً استفاده شده است',
                'max_length': 'اسلاگ نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد',
            },
            'cover': {
                'required': 'آپلود تصویر کاور الزامی است',
                'invalid_image': 'فایل ارسالی باید یک تصویر معتبر باشد',
            },
            'video_url': {
                'required': 'وارد کردن لینک ویدیو الزامی است',
                'invalid': 'لینک وارد شده معتبر نیست',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widget attributes
        self.fields['user'].widget.attrs.update({'class': 'form-select'})
        self.fields['product'].widget.attrs.update({'class': 'form-select', 'multiple': 'multiple'})
        self.fields['title_en'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Video title in English'})
        self.fields['title_fa'].widget.attrs.update({'class': 'form-control', 'placeholder': 'عنوان ویدیو به فارسی'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control', 'placeholder': 'اسلاگ ویدیو'})
        self.fields['cover'].widget.attrs.update({'class': 'form-control'})
        self.fields['video_url'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'https://example.com/video'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'توضیحات درباره ویدیو...'
        })

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        # You can add additional URL validation here if needed
        return video_url

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            # If slug is empty, it will be generated from title_en in the model's save()
            return slug
        return slug.lower()  # Ensure slug is lowercase



# continue coding ...........