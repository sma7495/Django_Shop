# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model


from ...models import Product, ProductCategory, ProductImage, ProductGuarantee, ProductColor, ProductSpecifications, ProductVideos


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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'created_date', 'updated_date']
        read_only_fields = ['id', 'created_date', 'updated_date']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Optionally add the full URL for the image if needed
        request = self.context.get('request')
        if request and instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation


class ProductGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGuarantee
        fields = [
            'id',
            'title_en',
            'title_fa',
            'slug',
            'description',
            'created_date',
            'updated_date'
        ]
        read_only_fields = ['id', 'slug', 'created_date', 'updated_date']
        extra_kwargs = {
            'title_en': {'required': True},
            'title_fa': {'required': True},
            'slug': {'required': False}  # Slug is auto-generated if not provided
        }

    def validate(self, data):
        """
        You can add any cross-field validation here if needed.
        For example, ensure slug is unique (though the model handles this)
        """
        return data

    def create(self, validated_data):
        """
        The default create() will work fine since we handle slug in model's save()
        """
        return ProductGuarantee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the instance. If title_en changes, the slug will update automatically
        through the model's save() method.
        """
        instance.title_en = validated_data.get('title_en', instance.title_en)
        instance.title_fa = validated_data.get('title_fa', instance.title_fa)
        instance.description = validated_data.get('description', instance.description)
        
        # Save will handle any slug updates if title_en changed
        instance.save()
        return instance


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = [
            'id',
            'title_en',
            'title_fa',
            'slug',
            'created_date',
            'updated_date'
        ]
        read_only_fields = ['id', 'slug', 'created_date', 'updated_date']
        extra_kwargs = {
            'title_en': {'required': True},
            'title_fa': {'required': True},
            'slug': {'required': False}  # Auto-generated if not provided
        }

    def validate(self, data):
        """
        Add any cross-field validation if needed
        """
        return data

    def create(self, validated_data):
        """
        Default create is fine - model's save() handles slug generation
        """
        return ProductColor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update instance - slug will auto-update if title_en changes
        """
        instance.title_en = validated_data.get('title_en', instance.title_en)
        instance.title_fa = validated_data.get('title_fa', instance.title_fa)
        instance.save()
        return instance


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = [
            'id',
            'product',
            'title_en',
            'title_fa',
            'value',
            'created_date',
            'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']
        extra_kwargs = {
            'product': {'required': True},
            'title_en': {'required': True},
            'title_fa': {'required': True},
            'value': {'required': True}
        }

    def validate(self, data):
        """
        Add any custom validation logic here if needed
        """
        return data

    def to_representation(self, instance):
        """
        Customize the representation if needed
        For example, you might want to nest product details
        """
        representation = super().to_representation(instance)
        
        # If you want to include minimal product info in the representation
        representation['product'] = {
            'id': instance.product.id,
            'name': str(instance.product)  # Assuming Product model has __str__ defined
        }
        return representation

class ProductVideosDetailSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # Optional: specify how users should be displayed
        label='Select User'
    )
    cover_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVideos
        fields = [
            'id',
            'user',
            'product',
            'title_en',
            'title_fa',
            'slug',
            'cover',
            'cover_url',
            'video_url',
            'description',
            'created_date',
            'updated_date'
        ]
        read_only_fields = fields
    
    def get_cover_url(self, obj):
        if obj.cover and hasattr(obj.cover, 'url'):
            return obj.cover.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    # SerializerMethodField for computed properties
    discounted_price = serializers.SerializerMethodField()
    
    # Nested serializers for related fields
    #user = UserSerializer(read_only=True)
    #category = ProductCategorySerializer(many=True, read_only=True)
    other_images = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    videos_urls = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField(required=False)
    guarantee = serializers.SerializerMethodField(required=False)
    # Custom field for image URL
    image_url = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # Optional: specify how users should be displayed
        label='Select User'
    )
    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'title_en',
            'title_fa',
            'slug',
            'image',
            'other_images',
            'guarantee',
            'color',
            'specifications',
            'image_url',
            'videos_urls',
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
            'user' : {'read_only': True}, 
            'color': {'required': False},
            'guarantee': {'required': False},
        }
        
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        
        if request and request.method in ['PUT', 'PATCH']:
            if request.user and (request.user.is_staff or request.user.is_superuser):
                fields['user'].read_only = False
        return fields

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
    
    def get_color(self, obj):
        if obj.color.exists():  # Assuming color is a ManyToManyField
            return ProductColorSerializer(obj.color.all(), many=True).data
        return None  # or [] for empty list

    def get_guarantee(self, obj):
        if obj.guarantee:  # Assuming guarantee is a ForeignKey and can be None
            return ProductGuaranteeSerializer(obj.guarantee).data
        return None
    
    def get_other_images(self, obj):
        
        images = ProductImage.objects.filter(product = obj.id)
        serializer = ProductImageSerializer(images ,many=True)
        return serializer.data
    
    def get_specifications(self, obj):
        specs = ProductSpecifications.objects.filter(product = obj.id)
        serializer = ProductSpecificationsSerializer(specs ,many=True)
        return serializer.data  
    def get_videos_urls(self,obj):
        videos = ProductVideos.objects.filter(product = obj.id)
        serializer = ProductVideosDetailSerializer(videos, many=True)
        return serializer.data
    
    def validate(self, data):
        """Custom validation for the product"""
        # Ensure discount percent is valid (though model already validates)
        if 'discount_percent' in data and data['discount_percent'] > 100:
            raise serializers.ValidationError("Discount percent cannot exceed 100%")
        
        # Add any other cross-field validation here
        return data
    
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        
        # Handle category
        rep["category"] = ProductCategorySerializer(
            instance.category.all(), many=True
        ).data if hasattr(instance, 'category') else []
        
        # Handle guarantee
        rep["guarantee"] = ProductGuaranteeSerializer(
            instance.guarantee
        ).data if instance.guarantee else None
        
        # Handle color
        rep["color"] = ProductColorSerializer(
            instance.color.all(), many=True
        ).data if hasattr(instance, 'color') else []
        
        return rep
    
    # def validate_category(self, value):
    #     if not value:  # Check if the list is empty
    #         raise serializers.ValidationError("At least one category must be selected.")
        
    #     # Optional: Check if all categories exist in database
    #     existing_categories = ProductCategory.objects.filter(id__in=[c.id for c in value])
    #     if len(existing_categories) != len(value):
    #         raise serializers.ValidationError("One or more categories do not exist.")
        
    #     return value
    
    
    
# continue coideing ...............