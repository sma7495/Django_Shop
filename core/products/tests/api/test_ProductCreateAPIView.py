from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from io import BytesIO

from ...models import Product, ProductCategory, ProductColor, ProductGuarantee
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductCreateAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.regular_user = User.objects.create_user(
            email='user@example.com',
            password='testpass123',
            is_staff=False
        )
        cls.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            type = 2,
        )
        cls.super_user = User.objects.create_superuser(
            email='superuser@example.com',
            password='superpass123'
        )
        cls.test_category = ProductCategory.objects.create(
            title_en='Test Category',
            title_fa='دسته بندی تستی'
        )
        cls.test_color = ProductColor.objects.create(
            title_en='Test Category',
            title_fa='دسته بندی تستی'
        )
        cls.test_guarantee = ProductGuarantee.objects.create(
            title_en='Test Category',
            title_fa='دسته بندی تستی',
            description = 'test'
        )
        
        # Sample valid product data with image
        cls.valid_product_data = {
            'title_en': 'Test Product',
            'title_fa': 'محصول آزمایشی',
            'description': 'Test description',
            'brief_description': 'Brief test',
            'stock': 10,
            'price': 1000,
            'discount_percent': 10,
            'status': 'published',
            'category': cls.test_category.id, # Add category ID
            'color': cls.test_color.id, 
            'guarantee': cls.test_guarantee.id  


        }

    def setUp(self):
        self.url = reverse('products:api:create')
        self.client = APIClient()

    def create_test_image(self):
        """Helper method to create a test image"""
        image = Image.new('RGB', (100, 100), color='red')
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            'test_image.jpg',
            image_file.getvalue(),
            content_type='image/jpeg'
        )
        
    def test_admin_can_create_product(self):
        """Test that admin users can create products"""
        self.client.force_authenticate(user=self.admin_user)
        
        data = self.valid_product_data.copy()
        data['image'] = self.create_test_image()
        
        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().user, self.admin_user)
        self.assertTrue(Product.objects.first().image)  # Check that image exists

    def test_product_creation_requires_image(self):
        """Test that product creation fails without an image"""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.post(self.url, self.valid_product_data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('image', response.data)  # Check that error mentions image field


    def test_product_creation_requires_category(self):
        """Test that product creation fails without a category"""
        self.client.force_authenticate(user=self.admin_user)
        
        invalid_data = self.valid_product_data.copy()
        invalid_data.pop('category')
        invalid_data['image'] = self.create_test_image()
        
        response = self.client.post(self.url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)  # Check that error mentions category field
        
        
    def test_superuser_can_create_product(self):
        """Test that superusers can create products"""
        self.client.force_authenticate(user=self.super_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_regular_user_cannot_create_product(self):
        """Test that regular users cannot create products"""
        self.client.force_authenticate(user=self.regular_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 0)
        

    def test_unauthenticated_user_cannot_create_product(self):
        """Test that unauthenticated users cannot create products"""
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_creation_with_valid_data(self):
        """Test product creation with complete valid data"""
        self.client.force_authenticate(user=self.admin_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title_en'], self.valid_product_data['title_en'])
        self.assertEqual(response.data['user'], self.admin_user.id)

    def test_product_creation_with_missing_required_fields(self):
        """Test that missing required fields return 400"""
        self.client.force_authenticate(user=self.admin_user)
        
        invalid_data = self.valid_product_data.copy()
        del invalid_data['title_en']  # Remove required field
        invalid_data["image"] = self.create_test_image()
        response = self.client.post(self.url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title_en', response.data)  # Should show error for missing field

    def test_product_creation_with_invalid_discount(self):
        """Test that discount > 100 is rejected"""
        self.client.force_authenticate(user=self.admin_user)
        invalid_data = self.valid_product_data.copy()
        invalid_data['discount_percent'] = 110  # Invalid discount
        invalid_data["image"] = self.create_test_image()
        response = self.client.post(self.url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('discount_percent', response.data)

    def test_automatic_user_assignment(self):
        """Test that the user is automatically set to the requesting user"""
        self.client.force_authenticate(user=self.admin_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.first()
        self.assertEqual(product.user, self.admin_user)

    def test_slug_auto_generation(self):
        """Test that slug is automatically generated from title_en"""
        self.client.force_authenticate(user=self.admin_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.first()
        self.assertIn('test-product' , product.slug )  # slugify('Test Product')

    def test_discounted_price_calculation(self):
        """Test that discounted_price is calculated correctly"""
        self.client.force_authenticate(user=self.admin_user)
        data = self.valid_product_data.copy()
        data["image"] = self.create_test_image()
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['discounted_price']), 900.0)  # 1000 - 10%