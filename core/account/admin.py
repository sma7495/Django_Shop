from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Address

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_active",
        "type",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    model = User
    list_display = ("user", "first_name", "last_name")


admin.site.register(Profile, ProfileAdmin)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('profile', 'state', 'city', 'zip_code', 'created_date')
    list_filter = ('state', 'city', 'created_date')
    search_fields = ('profile__user__email','state', 'city', 'zip_code', 'address')
    raw_id_fields = ('profile',)  # Better for performance with many users
    ordering = ('-created_date',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('profile',)
        }),
        ('Address Details', {
            'fields': ('state', 'city', 'address', 'zip_code')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    readonly_fields = ('created_date', 'updated_date')  # Prevent editing of timestamps