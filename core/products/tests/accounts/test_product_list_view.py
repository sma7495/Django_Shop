from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.test import TestCase, override_settings, RequestFactory
import os
from django.conf import settings
import shutil


from ...models import Product, ProductCategory, ProductColor, ProductGuarantee

User = get_user_model()


# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductListViewTest(TestCase):
    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile('test.jpg', file.getvalue(), 'image/jpeg')
    
    def setUp(self):
        # Create test users
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
            is_active=True,
            type=2  # type = admin
        )
        self.regular_user = User.objects.create_user(
            email='regular@example.com',
            password='testpass123',
            is_active=True,
        )
        
        # Create test categories and colors
        self.category1 = ProductCategory.objects.create(
            title_en='Electronics',
            title_fa='الکترونیک',
            slug='electronics'
        )
        self.category2 = ProductCategory.objects.create(
            title_en='Clothing',
            title_fa='لباس',
            slug='clothing'
        )
        
        self.color1 = ProductColor.objects.create(
            title_en='Red',
            title_fa='قرمز',
            slug='red'
        )
        self.color2 = ProductColor.objects.create(
            title_en='Blue',
            title_fa='آبی',
            slug='blue'
        )
        
        # Create test products
        self.product1 = Product.objects.create(
            title_en='Smartphone',
            title_fa='تلفن هوشمند',
            description='High-end smartphone',
            price=1000,
            discount_percent=10,
            slug='smartphone',
            status='published',
            user=self.superuser,
            image = self.create_test_image(),
        )
        self.product1.category.add(self.category1)
        self.product1.color.add(self.color1)
        
        self.product2 = Product.objects.create(
            title_en='T-Shirt',
            title_fa='تی شرت',
            description='Cotton t-shirt',
            price=20,
            discount_percent=0,
            slug='t-shirt',
            status='published',
            user=self.superuser,
            image = self.create_test_image(),
        )
        self.product2.category.add(self.category2)
        self.product2.color.add(self.color2)
        
        self.product3 = Product.objects.create(
            title_en='Laptop',
            title_fa='لپ تاپ',
            description='Gaming laptop',
            price=2000,
            discount_percent=15,
            slug='laptop',
            status='draft',
            user=self.superuser,
            image = self.create_test_image(),

        )
        self.product3.category.add(self.category1)
        self.product3.color.add(self.color1)
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
        
    def tearDown(self):
        # Clean up the test media directory
        try:
            shutil.rmtree(TEST_MEDIA_ROOT)
        except FileNotFoundError:
            pass   
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/product_list.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:list_product')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(response.status_code, 200)
    
    def test_queryset_returns_all_products_by_default(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(len(response.context['products']), 3)
        self.assertQuerySetEqual(
            response.context['products'],
            [self.product3, self.product2, self.product1],  # Default ordering is by -id
            transform=lambda x: x
        )
    
    def test_search_functionality(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Search by English title
        response = self.client.get(reverse('products:accounts:list_product'), {'search': 'Smartphone'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product1)
        
        # Search by Farsi title
        response = self.client.get(reverse('products:accounts:list_product'), {'search': 'تلفن'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product1)
        
        # Search by description
        response = self.client.get(reverse('products:accounts:list_product'), {'search': 'Cotton'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product2)
        
        # Search with no results
        response = self.client.get(reverse('products:accounts:list_product'), {'search': 'nonexistent'})
        self.assertEqual(len(response.context['products']), 0)
    
    def test_category_filter(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Filter by category1
        response = self.client.get(reverse('products:accounts:list_product'), {'category': 'electronics'})
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product3, response.context['products'])
        
        # Filter by category2
        response = self.client.get(reverse('products:accounts:list_product'), {'category': 'clothing'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product2)
    
    def test_color_filter(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Filter by color1
        response = self.client.get(reverse('products:accounts:list_product'), {'color': 'red'})
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product3, response.context['products'])
        
        # Filter by color2
        response = self.client.get(reverse('products:accounts:list_product'), {'color': 'blue'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product2)
    
    def test_price_range_filter(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Min price filter
        response = self.client.get(reverse('products:accounts:list_product'), {'min_price': 100})
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product3, response.context['products'])
        
        # Max price filter
        response = self.client.get(reverse('products:accounts:list_product'), {'max_price': 100})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product2)
        
        # Both min and max price
        response = self.client.get(reverse('products:accounts:list_product'), {'min_price': 500, 'max_price': 1500})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product1)
    
    def test_discount_filter(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Products with discount
        response = self.client.get(reverse('products:accounts:list_product'), {'has_discount': 'on'})
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product3, response.context['products'])
    
    def test_draft_filter(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Draft products only
        response = self.client.get(reverse('products:accounts:list_product'), {'is_draft': 'on'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0], self.product3)
    
    def test_combined_filters(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Combined filters
        response = self.client.get(reverse('products:accounts:list_product'), {
            'category': 'electronics',
            'color': 'red',
            'has_discount': 'on',
            'min_price': 500
        })
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product3, response.context['products'])
    
    def test_pagination(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create enough products to test pagination
        for i in range(15):
            Product.objects.create(
                title_en=f'Product {i}',
                title_fa=f'محصول {i}',
                price=100 + i,
                status='published',
                user=self.superuser,
                image = self.create_test_image(),
            )
        
        # First page should have 10 products
        response = self.client.get(reverse('products:accounts:list_product'))
        self.assertEqual(len(response.context['products']), 10)
        self.assertTrue(response.context['is_paginated'])
        
        # Second page should have the remaining 8 products (3 original + 15 new - 10 on first page)
        response = self.client.get(reverse('products:accounts:list_product'), {'page': 2})
        self.assertEqual(len(response.context['products']), 8)
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'))
        
        # Test context variables
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['selected_category'], None)
        self.assertEqual(response.context['selected_color'], None)
        self.assertEqual(response.context['min_price'], None)
        self.assertEqual(response.context['max_price'], None)
        self.assertEqual(response.context['has_discount'], None)
        self.assertEqual(response.context['is_draft'], None)
        
        # Test filter dropdown options
        self.assertQuerySetEqual(
            response.context['categories'],
            [self.category1, self.category2],
            transform=lambda x: x,
            ordered=False
        )
        self.assertQuerySetEqual(
            response.context['colors'],
            [self.color1, self.color2],
            transform=lambda x: x,
            ordered=False
        )
    
    def test_context_data_with_filters(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_product'), {
            'search': 'phone',
            'category': 'electronics',
            'color': 'red',
            'min_price': '500',
            'max_price': '1500',
            'has_discount': 'on',
            'is_draft': 'on'
        })
        
        # Test context variables with filters
        self.assertEqual(response.context['search_query'], 'phone')
        self.assertEqual(response.context['selected_category'], 'electronics')
        self.assertEqual(response.context['selected_color'], 'red')
        self.assertEqual(response.context['min_price'], '500')
        self.assertEqual(response.context['max_price'], '1500')
        self.assertEqual(response.context['has_discount'], 'on')
        self.assertEqual(response.context['is_draft'], 'on')