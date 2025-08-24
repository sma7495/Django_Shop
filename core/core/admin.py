# admin.py
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.html import format_html
import json

class SessionAdmin(admin.ModelAdmin):
    def session_data_formatted(self, obj):
        decoded_data = obj.get_decoded()
        formatted_json = json.dumps(decoded_data, indent=2, ensure_ascii=False)
        return format_html('<pre>{}</pre>', formatted_json)
    
    session_data_formatted.short_description = 'Session Data (Formatted)'
    
    def user_info(self, obj):
        decoded_data = obj.get_decoded()
        user_id = decoded_data.get('_auth_user_id')
        if user_id:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
                return f"{user.username} ({user.email})"
            except User.DoesNotExist:
                return f"User ID: {user_id} (not found)"
        return "Anonymous"
    
    user_info.short_description = 'User'
    
    list_display = ['session_key', 'user_info', 'expire_date']
    readonly_fields = ['session_key', 'session_data_formatted', 'user_info', 'expire_date']
    exclude = ['session_data']
    ordering = ['-expire_date']
    
    # Add search functionality
    search_fields = ['session_key']
    
    # Add filters
    list_filter = ['expire_date']

admin.site.register(Session, SessionAdmin)