from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',  # Notice the 'r' prefix
                message='Phone number must be 11 digits starting with 09',
                code='invalid_phone'
            ),
        ]
    )
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class SingletonModel(models.Model): # this class is to force user save only one record in some table
    """Base model to ensure only one instance exists."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs): # A new record always override existing record
        self.pk = 1  # Force primary key to always be 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls): # for give this record
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class AboutUs(SingletonModel): # enheritance from above class that save only one record
    slogan = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='website/about_us/', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Us Page"

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"


class Characteristic(SingletonModel):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='website/logo/', null=True)
    # Iranian mobile number (e.g., 09123456789)
    mobile_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="Mobile number must be 11 digits starting with '09' (e.g., 09123456789)."
            )
        ]
    )
    
    # Tehran office number (e.g., 02187654321)
    office_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^021\d{8}$',
                message="Office number must start with '021' followed by 8 digits (e.g., 02187654321)."
            )
        ]
    )
    
    address = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact Information: {self.name}"

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"


class TermsConditions(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=False)  # Default False to prevent auto-activation
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

    def clean(self):
        # Validation rules
        if len(self.title) < 10:
            raise ValidationError("Title must be at least 10 characters long.")

    class Meta:
        verbose_name = "Terms & Conditions"
        verbose_name_plural = "Terms & Conditions"
        ordering = ['-is_active', '-updated_date']


class FAQ(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(10, "Title must be at least 10 characters.")]
    )
    answer = models.TextField(
        validators=[MinLengthValidator(20, "Answer must be at least 20 characters.")]
    )
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-is_active', '-updated_date']
        indexes = [
            models.Index(fields=['is_active', 'title']),
        ]


#code..