from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from .validators import validate_english, validate_persian  # Import validators

User = get_user_model()

def product_image_upload_path(instance, filename):
    """Upload images to: /media/products/<slug>/<filename>"""
    return f"products/{instance.slug}/{filename}"

def validate_discount_percent(value):
    if value > 100:
        raise ValidationError("Discount percentage cannot exceed 100%.")
    if value < 0:
        raise ValidationError("Discount percentage cannot be negative.")
class Product(models.Model):
    # Status Choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='products')
    title_en = models.CharField(
        max_length=255,
        verbose_name='English Title',
        validators=[validate_english]  # English validator
    )
    title_fa = models.CharField(
        max_length=255,
        verbose_name='Persian Title',
        validators=[validate_persian]  # Persian validator
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to=product_image_upload_path)  # Uses slug in path
    description = models.TextField()
    brief_description = models.TextField()  # Fixed typo from "brif_description"
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[validate_discount_percent]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    category = models.ManyToManyField(to="ProductCategory", null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create slug from English title if not provided
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        """Calculate and return the discounted price"""
        return self.price * (1 - self.discount_percent / 100)


def product_image_slug_upload_path(instance, filename):
    """Upload path: products/<product_slug>/images/<filename>"""
    return f"products/{instance.product.slug}/images/{filename}"

class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',  # or use your app name like 'app.Product'
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to=product_image_slug_upload_path,
        verbose_name='Product Image'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['-created_date']

    def __str__(self):
        return f"Image for {self.product.title_en} (ID: {self.id})"


class ProductCategory(models.Model):
    title_en = models.CharField(
        max_length=255,
        verbose_name='English Title',
        validators=[validate_english]  # English validator
    )
    title_fa = models.CharField(
        max_length=255,
        verbose_name='Persian Title',
        validators=[validate_persian]  # Persian validator
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        allow_unicode=True  # Supports Persian characters in slugs
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['-created_date']
        unique_together = [['slug',]]  # Slug must be unique per product

    def __str__(self):
        return f"{self.title_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from English title if not provided
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)


# Create your models here.
