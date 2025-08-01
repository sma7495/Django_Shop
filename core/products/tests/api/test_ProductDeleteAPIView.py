from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from products.models import Product, ProductCategory
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductDeleteAPIViewTests(APITestCase):
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

        # Create test category
        cls.test_category = ProductCategory.objects.create(
            title_en='Test Category',
            title_fa='دسته بندی تستی',
            slug='test-category'
        )

        # Create test products
        cls.product1 = Product.objects.create(
            title_en='Product 1',
            title_fa='محصول ۱',
            description='Test description',
            brief_description='Brief test',
            stock=10,
            price=1000,
            discount_percent=10,
            status='published',
            user=cls.regular_user  # Owned by regular user
        )
        cls.product1.category.set([cls.test_category])  # Proper way to set many-to-many

        cls.product2 = Product.objects.create(
            title_en='Product 2',
            title_fa='محصول ۲',
            description='Test description',
            brief_description='Brief test',
            stock=5,
            price=2000,
            discount_percent=15,
            status='published',
            user=cls.admin_user  # Owned by admin user
        )
        cls.product2.category.set([cls.test_category])  # Proper way to set many-to-many

    def setUp(self):
        self.client = APIClient()

    def test_super_user_can_delete_any_product(self):
        """Test that admin users can delete any product"""
        self.client.force_authenticate(user=self.super_user)
        url = reverse('products:api:delete', kwargs={'pk': self.product1.pk})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())

    def test_owner_can_delete_own_product(self):
        """Test that product owners can delete their own products"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:api:delete', kwargs={'pk': self.product1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())

    def test_regular_user_cannot_delete_other_products(self):
        """Test that regular users cannot delete products they don't own"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('products:api:delete', kwargs={'pk': self.product2.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product2.pk).exists())

    def test_unauthenticated_user_cannot_delete_products(self):
        """Test that unauthenticated users cannot delete products"""
        url = reverse('products:api:delete', kwargs={'pk': self.product1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(pk=self.product1.pk).exists())

    def test_delete_nonexistent_product_returns_404(self):
        """Test that deleting a non-existent product returns 404"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:api:delete', kwargs={'pk': 9999})  # Non-existent ID
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_delete_returns_custom_message(self):
        """Test that successful deletion returns the custom success message"""
        self.client.force_authenticate(user=self.super_user)
        url = reverse('products:api:delete', kwargs={'pk': self.product1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.data, {"detail": "Product deleted successfully."})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)