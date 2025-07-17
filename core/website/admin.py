from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('name', 'email', 'phone_number', 'subject', 'created_date', 'is_read')
    
    # Make 'is_read' editable directly from list view
    list_editable = ('is_read',)
    
    # Enable filtering by these fields
    list_filter = ('is_read', 'created_date')
    
    # Enable search for these fields
    search_fields = ('name', 'email', 'subject')
    
    # Fields to show in edit form (in this order)
    fields = ('name', 'email', 'phone_number', 'subject', 'message', 'is_read')
    
    # Automatically set dates (no user input)
    readonly_fields = ('created_date', 'updated_date')