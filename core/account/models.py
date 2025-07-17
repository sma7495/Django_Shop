from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='customer',
        verbose_name='User Type'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="image/profile/", blank=True, null=True)
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
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Address(models.Model):
    """Model representing a user's address with Iranian zip code validation."""
    
    # Iranian zip code validator (10 digits)
    iran_zip_code_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Zip code must be 10 digits (Iranian format)'
    )
    
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Profile'
    )
    state = models.CharField(
        max_length=50,
        verbose_name='State/Province'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='City'
    )
    address = models.TextField(
        verbose_name='Street Address'
    )
    zip_code = models.CharField(
        max_length=10,
        validators=[iran_zip_code_validator],
        verbose_name='Zip Code'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation Date'
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Update Date'
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.email} - {self.city}, {self.state}"