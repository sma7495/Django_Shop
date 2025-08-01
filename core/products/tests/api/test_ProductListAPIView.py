from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ...models import Product
from ...api.v1.serializers import ProductSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductListAPIViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user1 = User.objects.create_user(
            email='seller1@example.com',
            password='testpass123',
            is_staff=False
        )
        cls.admin = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )

        # Create test products
        cls.product1 = Product.objects.create(
            user=cls.user1,
            title_en='Product A',
            title_fa='محصول الف',
            status='published',
            price=1000,
            discount_percent=10,
            stock=10
        )
        cls.product2 = Product.objects.create(
            user=cls.user1,
            title_en='Product B',
            title_fa='محصول ب',
            status='published',
            price=2000,
            discount_percent=20,
            stock=5
        )
        cls.product3 = Product.objects.create(
            user=cls.user1,
            title_en='Product C',
            title_fa='محصول ج',
            status='draft',  # Should not appear in results
            price=3000,
            discount_percent=0,
            stock=3
        )
    def setUp(self):
        # This runs before every test method
        self.url = reverse('products:api:list')
        
        
    def test_get_published_products_only(self):
        """Test that only published products are returned"""
        url = self.url
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Only 2 published products
        
        products = Product.objects.filter(status='published')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_default_ordering(self):
        """Test that products are ordered by -created_date by default"""
        url = self.url
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.product2.id)
        self.assertEqual(response.data['results'][1]['id'], self.product1.id)

    def test_price_ordering(self):
        """Test ordering by price"""
        url = self.url
        response = self.client.get(url, {'ordering': 'price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.product1.id)
        self.assertEqual(response.data['results'][1]['id'], self.product2.id)

    def test_descending_price_ordering(self):
        """Test ordering by -price"""
        url = self.url
        response = self.client.get(url, {'ordering': '-price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.product2.id)
        self.assertEqual(response.data['results'][1]['id'], self.product1.id)

    def test_discount_percent_ordering(self):
        """Test ordering by discount_percent"""
        url = self.url
        response = self.client.get(url, {'ordering': 'discount_percent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.product1.id)
        self.assertEqual(response.data['results'][1]['id'], self.product2.id)

    def test_invalid_ordering_field(self):
        """Test that invalid ordering field returns 400"""
        url = self.url
        response = self.client.get(url, {'ordering': 'invalid_field'})
        
        # return default ordering
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.product2.id)
        self.assertEqual(response.data['results'][1]['id'], self.product1.id)

    def test_pagination(self):
        """Test that pagination is working"""
        # Create enough products to trigger pagination
        for i in range(15):
            Product.objects.create(
                user=self.user1,
                title_en=f'Product {i}',
                title_fa=f'محصول {i}',
                status='published',
                price=1000 + i,
                stock=10
            )
        
        url = self.url
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Default page size

    def test_unauthenticated_access(self):
        """Test that unauthenticated users can access the list"""
        url = self.url
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)