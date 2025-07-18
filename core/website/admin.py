from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, AboutUs, Characteristic, TermsConditions, FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_answer', 'is_active', 'updated_date')
    list_filter = ('is_active',)
    search_fields = ('title', 'answer')
    list_editable = ('is_active',)
    readonly_fields = ('created_date', 'updated_date')
    actions = ['activate_all', 'deactivate_all']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'answer', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        })
    )

    def truncated_answer(self, obj):
        return format_html(
            '<span title="{}">{}...</span>',
            obj.answer,
            obj.answer[:50] if len(obj.answer) > 50 else obj.answer
        )
    truncated_answer.short_description = "Answer Preview"

    def activate_all(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} FAQs activated")
    activate_all.short_description = "Activate selected"

    def deactivate_all(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} FAQs deactivated")
    deactivate_all.short_description = "Deactivate selected"


@admin.register(TermsConditions)
class TermsConditionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_date', 'updated_date')
    list_editable = ('is_active',)  # Allow quick toggling
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    # Disable "Add" button if instance exists
    def has_add_permission(self, request):
        return not Characteristic.objects.exists()
    
    # Optional: Prevent deletion of the singleton instance
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deletion

    # Admin display settings
    list_display = ['name', 'contact_email', 'mobile_number', 'office_number']
    readonly_fields = ['created_date', 'updated_date']

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    # Ensure that only one instance can be created
    def has_add_permission(self, request):
        # Disable the "Add" button if an instance already exists
        if AboutUs.objects.exists():
            return False
        return super().has_add_permission(request)

    # Customize the admin display
    list_display = ['__str__', 'slogan', 'created_date', 'updated_date']
    readonly_fields = ['created_date', 'updated_date']

    # Optional: Prevent deletion of the singleton instance
    def has_delete_permission(self, request, obj=None):
        return False  # Disable deletion
    

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