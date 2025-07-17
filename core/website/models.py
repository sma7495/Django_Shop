from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

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