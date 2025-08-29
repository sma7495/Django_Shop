from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa']
    search_fields = ['title_en', 'title_fa']
    prepopulated_fields = {'slug': ('title_en',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'slug']
    search_fields = ['title_en', 'title_fa']
    prepopulated_fields = {'slug': ('title_en',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title_en', 
        'status', 
        'is_active', 
        'user', 
        'created_date', 
        'views',
        'featured'
    ]
    list_filter = ['status', 'is_active', 'featured', 'created_date', 'categories']
    search_fields = ['title_en', 'title_fa', 'content']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'created_date'
    filter_horizontal = ['tags', 'categories']
    readonly_fields = ['created_date', 'updated_date', 'published_date', 'views']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title_en', 'title_fa', 'slug', 'user')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'image', 'meta_description')
        }),
        ('Categorization', {
            'fields': ('tags', 'categories')
        }),
        ('Status & Dates', {
            'fields': ('status', 'featured', 'created_date', 'updated_date', 'published_date')
        }),
        ('Statistics', {
            'fields': ('views', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Set the user to the current user if it's a new post
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)