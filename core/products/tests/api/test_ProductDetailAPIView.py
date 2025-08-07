from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ...models import Product, ProductCategory
from ...api.v1.serializers import ProductSerializer
from ...api.v1.permissions import IsProductOwnerOrAdmin

User = get_user_model()


class ProductDetailAPIViewTests(APITestCase):
    
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
            type=2,
        )
        cls.super_user = User.objects.create_superuser(
            email='superuser@example.com',
            password='superpass123'
        )

        # Create test categories
        cls.category1 = ProductCategory.objects.create(
            title_en='Category 1',
            title_fa='دسته ۱',
            slug='category-1'
        )
        cls.category2 = ProductCategory.objects.create(
            title_en='Category 2',
            title_fa='دسته ۲',
            slug='category-2'
        )

        # Create test products
        cls.product = Product.objects.create(
            title_en='Product 1',
            title_fa='محصول ۱',
            description='Original description',
            brief_description='Brief original',
            stock=10,
            price=1000,
            discount_percent=10,
            status='draft',
            user=cls.regular_user
        )
        cls.product.category.set([cls.category1])

    def setUp(self):
        # URL for the product detail
        self.url = reverse('products:api:detail', kwargs={'pk': self.product.pk})

    def test_retrieve_product_unauthenticated(self):
        """Test that unauthenticated users can retrieve product details"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title_en'], self.product.title_en)
        
        # Check if serializer data matches
        # Create a request object for the serializer context
        request = response.wsgi_request  # Get the request from the test client response
        
        # Pass the request in the context
        serializer = ProductSerializer(
            self.product, 
            context={'request': request}  # Add request to context
        )
        self.assertEqual(response.data, serializer.data)



    def test_retrieve_product_authenticated(self):
        """Test that authenticated users can retrieve product details"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title_en'], self.product.title_en)


        # this test is for PATCH method ............
        
    # def test_update_product_by_owner(self):
    #     """Test that product owner can update the product"""
    #     self.client.force_authenticate(user=self.regular_user)
    #     data = {'title_en': 'Updated Name', 'price': 129000}
    #     response = self.client.patch(self.url, data)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.title_en, 'Updated Name')
    #     self.assertEqual(float(self.product.price), 129.99)



    # def test_update_product_by_admin(self):
    #     """Test that admin can update any product"""
    #     self.client.force_authenticate(user=self.admin)
    #     data = {'description': 'Admin updated description'}
    #     response = self.client.patch(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.description, 'Admin updated description')


    # def test_update_product_by_unauthorized_user(self):
    #     """Test that regular users cannot update others' products"""
    #     self.client.force_authenticate(user=self.regular_user)
    #     data = {'name': 'Unauthorized Update'}
    #     response = self.client.patch(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.product.refresh_from_db()
    #     self.assertNotEqual(self.product.name, 'Unauthorized Update')

    # def test_delete_product_by_owner(self):
    #     """Test that product owner can delete the product"""
    #     self.client.force_authenticate(user=self.owner)
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    # def test_delete_product_by_admin(self):
    #     """Test that admin can delete any product"""
    #     self.client.force_authenticate(user=self.admin)
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    # def test_delete_product_by_unauthorized_user(self):
    #     """Test that regular users cannot delete others' products"""
    #     self.client.force_authenticate(user=self.regular_user)
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    # def test_update_product_unauthenticated(self):
    #     """Test that unauthenticated users cannot update products"""
    #     data = {'name': 'Unauthenticated Update'}
    #     response = self.client.patch(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.product.refresh_from_db()
    #     self.assertNotEqual(self.product.name, 'Unauthenticated Update')

    # def test_delete_product_unauthenticated(self):
    #     """Test that unauthenticated users cannot delete products"""
    #     response = self.client.delete(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    # def test_view_count_increment(self):
    #     """Test that view count increments on GET requests"""
    #     initial_count = self.product.view_count
        
    #     # First request from unauthenticated user
    #     response = self.client.get(self.url)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.view_count, initial_count + 1)
        
    #     # Second request from different user
    #     self.client.force_authenticate(user=self.regular_user)
    #     response = self.client.get(self.url)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.view_count, initial_count + 2)
        
    #     # Request from owner shouldn't increment
    #     self.client.force_authenticate(user=self.owner)
    #     response = self.client.get(self.url)
    #     self.product.refresh_from_db()
    #     self.assertEqual(self.product.view_count, initial_count + 2)


    # def test_nonexistent_product(self):
    #     """Test requesting a product that doesn't exist"""
    #     invalid_url = reverse('product-detail', kwargs={'pk': 9999})
    #     response = self.client.get(invalid_url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_head_and_options_methods(self):
        """Test that HEAD and OPTIONS methods are allowed for anyone"""
        # Test HEAD
        response = self.client.head(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test OPTIONS
        response = self.client.options(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('PUT', response.data['actions'])
        # self.assertIn('PATCH', response.data['actions'])