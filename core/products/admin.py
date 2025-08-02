from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Product, ProductImage, ProductCategory, ProductGuarantee, ProductColor, ProductSpecifications, ProductVideos

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'title_en', 'title_fa', 'status', 'price', 'discount_percent', 'stock', 'created_date')
    list_filter = ('status', 'created_date', 'category')
    search_fields = ('title_en', 'title_fa', 'description')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('color', 'category')  # For better ManyToMany field interface
    readonly_fields = ('created_date', 'updated_date', 'discounted_price')
    fieldsets = (
        (None, {
            'fields': ('user', 'title_en', 'title_fa', 'slug', 'image', 'description', 'brief_description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'discount_percent', 'discounted_price', 'stock')
        }),
        ('Relations', {
            'fields': ('color', 'guarantee', 'category')
        }),
        ('Status & Dates', {
            'fields': ('status', 'created_date', 'updated_date')
        }),
    )

    def discounted_price(self, obj):
        return obj.discounted_price
    discounted_price.short_description = 'Current Price After Discount'


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

@admin.register(ProductGuarantee)
class ProductGuaranteeAdmin(admin.ModelAdmin):
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

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
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


@admin.register(ProductSpecifications)
class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_fa','created_date']
    list_filter = ['created_date']
    search_fields = ['title_en', 'title_fa']
    readonly_fields = ['created_date', 'updated_date']
    
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_fa', 'product')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductVideos)
class ProductVideosAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fa', 'user', 'created_date', 'updated_date')
    list_filter = ('created_date', 'updated_date', 'user')
    search_fields = ('title_en', 'title_fa', 'description')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('product',)  # For better many-to-many field display
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date', 'updated_date', 'display_cover')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'product', 'title_en', 'title_fa', 'slug')
        }),
        ('Media', {
            'fields': ('cover', 'display_cover', 'video_url')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Dates', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )

    def display_cover(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" width="150" />')
        return "No Cover"
    
    display_cover.short_description = 'Cover Preview'

# Register your models here.
