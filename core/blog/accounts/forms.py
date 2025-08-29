from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import jdatetime
from django.utils import timezone


from ..models import Post, Tag, Category



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title_en', 'title_fa', 'content', 'excerpt', 'image', 
            'status', 'tags', 'categories', 'featured', 'meta_description'
        ]
        widgets = {
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان انگلیسی پست را وارد کنید',
                'dir': 'ltr'
            }),
            'title_fa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان فارسی پست را وارد کنید',
                'dir': 'rtl'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'محتوای پست را وارد کنید',
                'rows': 10,
                'dir': 'rtl'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'خلاصه کوتاهی از پست (حداکثر 500 کاراکتر)',
                'rows': 3,
                'dir': 'rtl'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'status-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': 'multiple',
                'data-placeholder': 'تگ‌ها را انتخاب کنید'
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': 'multiple',
                'data-placeholder': 'دسته‌بندی‌ها را انتخاب کنید'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات متا برای SEO (حداکثر 160 کاراکتر)',
                'rows': 2,
                'dir': 'rtl'
            }),
        }
        labels = {
            'title_en': _('عنوان انگلیسی'),
            'title_fa': _('عنوان فارسی'),
            'content': _('محتوای پست'),
            'excerpt': _('خلاصه پست'),
            'image': _('تصویر اصلی'),
            'status': _('وضعیت انتشار'),
            'tags': _('تگ‌ها'),
            'categories': _('دسته‌بندی‌ها'),
            'featured': _('پست ویژه'),
            'meta_description': _('توضیحات متا'),
        }
        help_texts = {
            'title_en': _('عنوان پست به زبان انگلیسی (فقط حروف انگلیسی مجاز)'),
            'title_fa': _('عنوان پست به زبان فارسی (فقط حروف فارسی مجاز)'),
            'content': _('محتوای کامل پست به زبان فارسی'),
            'excerpt': _('خلاصه کوتاه پست که در لیست مطالب نمایش داده می‌شود (اختیاری)'),
            'image': _('تصویر شاخص پست با فرمت JPG, PNG یا GIF'),
            'status': _('وضعیت فعلی پست: پیش‌نویس، منتشر شده یا بایگانی شده'),
            'tags': _('تگ‌های مرتبط با پست (برای طبقه‌بندی بهتر)'),
            'categories': _('دسته‌بندی‌های اصلی پست (حداقل یک دسته‌بندی الزامی است)'),
            'featured': _('در صورت فعال بودن، پست در بخش مطالب ویژه نمایش داده می‌شود'),
            'meta_description': _('توضیحات مختصر برای موتورهای جستجو (اختیاری)'),
        }
        error_messages = {
            'title_en': {
                'required': _('عنوان انگلیسی الزامی است'),
                'max_length': _('عنوان انگلیسی نمی‌تواند بیش از 255 کاراکتر باشد')
            },
            'title_fa': {
                'required': _('عنوان فارسی الزامی است'),
                'max_length': _('عنوان فارسی نمی‌تواند بیش از 255 کاراکتر باشد')
            },
            'content': {
                'required': _('محتوای پست الزامی است')
            },
            'categories': {
                'required': _('حداقل یک دسته‌بندی باید انتخاب شود')
            },
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set querysets for many-to-many fields
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['categories'].queryset = Category.objects.all()
        
        # Make categories required
        self.fields['categories'].required = True
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['featured']:  # Skip checkbox
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'
        
        # Add RTL direction to Persian fields
        persian_fields = ['title_fa', 'content', 'excerpt', 'meta_description']
        for field_name in persian_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['dir'] = 'rtl'
        
        # Add LTR direction to English fields
        english_fields = ['title_en']
        for field_name in english_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['dir'] = 'ltr'

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise ValidationError(_('حداقل یک دسته‌بندی باید انتخاب شود'))
        return categories

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 100:
            raise ValidationError(_('محتوای پست باید حداقل 100 کاراکتر داشته باشد'))
        return content

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        content = cleaned_data.get('content')
        
        # Validate that published posts have content
        if status == Post.PUBLISHED and content and not content.strip():
            self.add_error('content', _('پست‌های منتشر شده باید محتوا داشته باشند'))
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the user if it's a new post
        if not instance.pk and self.user:
            instance.user = self.user
        
        if commit:
            instance.save()
            self.save_m2m()  # Save many-to-many relationships
        
        return instance


    """Form for searching posts"""
    STATUS_CHOICES = [
        ('', 'همه وضعیت‌ها'),
        (Post.DRAFT, 'پیش‌نویس'),
        (Post.PUBLISHED, 'منتشر شده'),
        (Post.ARCHIVED, 'بایگانی شده'),
    ]
    
    search = forms.CharField(
        required=False,
        label='جستجو',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در عنوان و محتوا...',
            'dir': 'rtl'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        label='وضعیت',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        label='دسته‌بندی',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    featured = forms.BooleanField(
        required=False,
        label='فقط مطالب ویژه',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        label='از تاریخ',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'از تاریخ...'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        label='تا تاریخ',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'تا تاریخ...'
        })
    )   

class PostSearchForm(forms.Form):
    """Form for searching posts"""
    STATUS_CHOICES = [
        ('', 'همه وضعیت‌ها'),
        (Post.DRAFT, 'پیش‌نویس'),
        (Post.PUBLISHED, 'منتشر شده'),
        (Post.ARCHIVED, 'بایگانی شده'),
    ]
    
    search = forms.CharField(
        required=False,
        label='جستجو',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در عنوان و محتوا...',
            'dir': 'rtl'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        label='وضعیت',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        label='دسته‌بندی',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    featured = forms.BooleanField(
        required=False,
        label='فقط مطالب ویژه',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        label='از تاریخ',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'از تاریخ...'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        label='تا تاریخ',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'تا تاریخ...'
        })
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title_en', 'title_fa']
        labels = {
            'title_en': _('عنوان انگلیسی'),
            'title_fa': _('عنوان فارسی'),
        }
        help_texts = {
            'title_en': _('عنوان به زبان انگلیسی وارد شود (فقط حروف انگلیسی)'),
            'title_fa': _('عنوان به زبان فارسی وارد شود'),
        }
        widgets = {
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان انگلیسی را وارد کنید',
                'dir': 'ltr'
            }),
            'title_fa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان فارسی را وارد کنید',
                'dir': 'rtl'
            }),
        }
    
    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en')
        # Additional validation if needed
        return title_en
    
    def clean_title_fa(self):
        title_fa = self.cleaned_data.get('title_fa')
        # Additional validation if needed
        return title_fa
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make slug field read-only in update form if needed
        # You can add slug field if you want to allow manual editing    

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title_en', 'title_fa']
        labels = {
            'title_en': _('عنوان انگلیسی'),
            'title_fa': _('عنوان فارسی'),
        }
        help_texts = {
            'title_en': _('عنوان به زبان انگلیسی وارد شود (فقط حروف انگلیسی)'),
            'title_fa': _('عنوان به زبان فارسی وارد شود'),
        }
        widgets = {
            'title_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان انگلیسی تگ را وارد کنید',
                'dir': 'ltr'
            }),
            'title_fa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان فارسی تگ را وارد کنید',
                'dir': 'rtl'
            }),
        }
    
    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en')
        
        # Check if we're updating an existing instance
        if self.instance and self.instance.pk:
            # Exclude the current instance from the query
            tag = Tag.objects.filter(title_fa__iexact=title_en).exclude(pk=self.instance.pk)
        else:
            # Creating a new instance - check all records
            tag = Tag.objects.filter(title_fa__iexact=title_en)
            
        if tag.exists():
            raise ValidationError(_('تگ با این عنوان انگلیسی از قبل وجود دارد'))
        return title_en
    
    def clean_title_fa(self):
        title_fa = self.cleaned_data.get('title_fa')
        
        # Check if we're updating an existing instance
        if self.instance and self.instance.pk:
            # Exclude the current instance from the query
            tag = Tag.objects.filter(title_fa__iexact=title_fa).exclude(pk=self.instance.pk)
        else:
            # Creating a new instance - check all records
            tag = Tag.objects.filter(title_fa__iexact=title_fa)
        
        if tag.exists():
            raise ValidationError(_('تگ با این عنوان فارسی از قبل وجود دارد'))
        
        return title_fa
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make slug field read-only in update form if needed
        # You can add slug field if you want to allow manual editing   

#continue ...........