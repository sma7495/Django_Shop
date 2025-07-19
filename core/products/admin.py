from django.contrib import admin
from django.utils.html import format_html

from .models import Product, ProductImage, ProductCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields displayed in the admin list view
    list_display = [
        'title_en',
        'title_fa',
        'user',
        'price',
        'discount_percent',
        'stock',
        'status',
        'created_date',
    ]

    # Search functionality (searches in these fields)
    search_fields = [
        'title_en',
        'title_fa',
        'description',
    ]

    # Filters for easy navigation
    list_filter = [
        'user',
        'status',
        'created_date',
        'stock',
    ]

    # Pre-populate slug from title_en
    prepopulated_fields = {'slug': ('title_en',)}

    # Fields grouping in edit view
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title_en', 'title_fa', 'slug', 'image', 'category'),
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_percent', 'stock'),
        }),
        ('Descriptions', {
            'fields': ('brief_description', 'description'),
        }),
    )

    # Auto-set the user to the current admin user when adding a product
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # If user isn't set, assign current admin
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # List view settings
    list_display = ['product', 'image_preview', 'created_date', 'updated_date']
    list_filter = ['product', 'created_date']
    search_fields = ['product__title_en', 'product__slug']
    readonly_fields = ['image_preview_large', 'created_date', 'updated_date']
    list_select_related = ['product']  # Optimize DB queries

    # Fields for add/edit view
    fieldsets = (
        (None, {
            'fields': ('product', 'image')
        }),
        ('Metadata', {
            'fields': ('image_preview_large', 'created_date', 'updated_date'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )

    # Thumbnail preview in list view
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

    # Larger preview in edit view
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;" />', obj.image.url)
        return "-"
    image_preview_large.short_description = 'Image Preview'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa', 'slug', 'created_date']
    list_filter = ['created_date']
    search_fields = ['title_en', 'title_fa']
    prepopulated_fields = {'slug': ('title_en',)}
    readonly_fields = ['created_date', 'updated_date']
    
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_fa', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
# Register your models here.
