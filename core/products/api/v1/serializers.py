# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model


from ...models import Product, ProductCategory


User = get_user_model()

class ProductCategorySerializer(serializers.ModelSerializer):
    # Add any computed fields if needed
    full_title = serializers.SerializerMethodField()
    # For the image URL if you add image field later
    # image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'title_en',
            'title_fa',
            'slug',
            'full_title',
            'created_date',
            'updated_date',
            # 'image_url',  # Uncomment if you add image field
        ]
        read_only_fields = [
            'id',
            'slug',
            'created_date',
            'updated_date',
            'full_title',
            # 'image_url',
        ]
        extra_kwargs = {
            'title_en': {'required': True},
            'title_fa': {'required': True},
        }

    def get_full_title(self, obj):
        """Returns both English and Persian titles together"""
        return f"{obj.title_en} / {obj.title_fa}"
    
    # Uncomment if you add image field to the model later
    # def get_image_url(self, obj):
    #     """Return absolute URL for the category image"""
    #     if obj.image and hasattr(obj.image, 'url'):
    #         request = self.context.get('request')
    #         if request is not None:
    #             return request.build_absolute_uri(obj.image.url)
    #         return obj.image.url
    #     return None

    def validate(self, data):
        """Custom validation for the category"""
        # Add any custom validation logic here
        # For example, you might want to ensure titles are not identical
        if 'title_en' in data and 'title_fa' in data:
            if data['title_en'] == data['title_fa']:
                raise serializers.ValidationError(
                    "English and Persian titles should not be identical"
                )
        return data

    def create(self, validated_data):
        """Handle category creation with slug generation"""
        # Slug will be automatically generated in the model's save() method
        return ProductCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Handle category update"""
        # If title_en changes, the slug should be regenerated
        if 'title_en' in validated_data:
            if instance.title_en != validated_data['title_en']:
                instance.slug = ''  # This will trigger slug regeneration in save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance



class ProductSerializer(serializers.ModelSerializer):
    # SerializerMethodField for computed properties
    discounted_price = serializers.SerializerMethodField()
    
    # Nested serializers for related fields
    #user = UserSerializer(read_only=True)
    category = ProductCategorySerializer(many=True, read_only=True)
    
    # Custom field for image URL
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'title_en',
            'title_fa',
            'slug',
            'image',
            'image_url',
            'description',
            'brief_description',
            'stock',
            'price',
            'discount_percent',
            'discounted_price',
            'status',
            'category',
            'created_date',
            'updated_date',
        ]
        read_only_fields = [
            'id',
            'slug',
            'created_date',
            'updated_date',
            'discounted_price',
            'image_url',
        ]
        extra_kwargs = {
            'image': {'write_only': True},  # Only used for uploads, not in responses
        }

    def get_discounted_price(self, obj):
        """Serialize the discounted_price property"""
        return float(obj.discounted_price) if obj.discounted_price else None

    def get_image_url(self, obj):
        """Return absolute URL for the product image"""
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def validate(self, data):
        """Custom validation for the product"""
        # Ensure discount percent is valid (though model already validates)
        if 'discount_percent' in data and data['discount_percent'] > 100:
            raise serializers.ValidationError("Discount percent cannot exceed 100%")
        
        # Add any other cross-field validation here
        return data