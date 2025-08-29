from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save

from .validators import validate_english, validate_persian

User = get_user_model()

class Category(models.Model):
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
    slug = models.SlugField(max_length=255, unique=True)
    # description = models.TextField(blank=True)
    # is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title_en"]
    
    def __str__(self):
        return self.title_en
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)



class Tag(models.Model):
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
    slug = models.SlugField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["title_en"]
    
    def __str__(self):
        return self.title_en
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)



class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]
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
    slug = models.SlugField(max_length=256, unique_for_date='created_date', blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text="Brief summary of the post")
    image = models.ImageField(upload_to="blog_images/%Y/%m/%d/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["-created_date"]
        indexes = [
            models.Index(fields=['-created_date', 'status']),
            models.Index(fields=['slug']),
        ]
        get_latest_by = "created_date"
        
    def __str__(self):
        return self.title_en
    
    def save(self, *args, **kwargs):
        # Generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title_en)
            
        # Set published_date when status changes to published
        if self.status == self.PUBLISHED and not self.published_date:
            self.published_date = timezone.now()
            self.is_active = True
        elif self.status != self.PUBLISHED:
            self.is_active = False
            
        # Generate excerpt from content if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:497] + '...' if len(self.content) > 500 else self.content
            
        # Generate meta description if not provided
        if not self.meta_description:
            self.meta_description = self.excerpt[:157] + '...' if len(self.excerpt) > 160 else self.excerpt
            
        super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse("blog:single-blog", kwargs={"pid": self.id, "slug": self.slug})
    
    def clean(self):
        # Validate that published posts have content
        if self.status == self.PUBLISHED and not self.content.strip():
            raise ValidationError({'content': 'Published posts must have content.'})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def is_published(self):
        return self.status == self.PUBLISHED and self.published_date <= timezone.now()

# to handle published date for draft and published posts..........
@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, **kwargs):
    """
    Signal handler to manage published_date based on post status.
    """
    # If post is being published for the first time
    if instance.status == Post.PUBLISHED and not instance.published_date:
        instance.published_date = timezone.now()
        # We need to save again since we're modifying the instance
        instance.save()
    
    # If post is being changed to draft and has a published_date
    elif instance.status == Post.DRAFT and instance.published_date:
        instance.published_date = None
        # We need to save again since we're modifying the instance
        instance.save()



# continue coding ..........