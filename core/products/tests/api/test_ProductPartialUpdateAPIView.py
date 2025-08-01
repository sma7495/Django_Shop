from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from products.models import Product, ProductCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductPartialUpdateAPIViewTests(APITestCase):
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
        cls.product1 = Product.objects.create(
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
        cls.product1.category.set([cls.category1])

        cls.product2 = Product.objects.create(
            title_en='Product 2',
            title_fa='محصول ۲',
            description='Original description',
            brief_description='Brief original',
            stock=20,
            price=2000,
            discount_percent=20,
            status='published',
            user=cls.admin_user
        )
        cls.product2.category.set([cls.category1])

    def setUp(self):
        self.client = APIClient()
        self.url = lambda pk: reverse('products:api:update', kwargs={'pk': pk})

    # Helper methods
    def get_product_data(self, product):
        return {
            'title_en': product.title_en,
            'title_fa': product.title_fa,
            'description': product.description,
            'brief_description': product.brief_description,
            'stock': product.stock,
            'price': product.price,
            'discount_percent': product.discount_percent,
            'status': product.status,
            'category': [c.id for c in product.category.all()],
            'user': product.user.id
        }

    # Partial Update Tests
    def test_owner_can_partially_update_own_product(self):
        """Product owner can partially update their product"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'title_en': 'Updated Title',
            'status': 'published'
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.title_en, 'Updated Title')
        self.assertEqual(self.product1.status, 'published')
        self.assertEqual(response.data['detail'], 'Product partially updated successfully.')


    def test_super_user_can_partially_update_any_product(self):
        """Admin can partially update any product"""
        self.client.force_authenticate(user=self.super_user)
        update_data = {
            'price': 1500,
            'user': self.admin_user.id  # Test admin changing owner
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.price, 1500)
        self.assertEqual(self.product1.user, self.admin_user)
        
        

    def test_regular_user_cannot_change_product_owner(self):
        """Regular user cannot change product owner"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'user': self.admin_user.id
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.user, self.regular_user)  # Should remain unchanged

    def test_regular_user_cannot_update_other_products(self):
        """Regular user cannot update products they don't own"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'title_en': 'Unauthorized Update'
        }
        
        response = self.client.patch(self.url(self.product2.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_update_products(self):
        """Unauthenticated users cannot update products"""
        update_data = {
            'title_en': 'Unauthenticated Update'
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_with_invalid_data(self):
        """Partial update with invalid data should fail"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'price': -100  # Invalid price
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_update_category_relationship(self):
        """Test updating category relationships"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'category': [self.category2.id]
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(list(self.product1.category.values_list('id', flat=True)), [self.category2.id])

    # Complete Update Tests
    def test_complete_update_by_owner(self):
        """Product owner can completely update their product"""
        self.client.force_authenticate(user=self.regular_user)
        update_data = {
            'title_en': 'Completely Updated',
            'title_fa': 'محصول کاملاً بروزرسانی شده',
            'description': 'New description',
            'brief_description': 'New brief',
            'stock': 50,
            'price': 5000,
            'discount_percent': 5,
            'status': 'published',
            'category': [self.category1.id]
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.title_en, 'Completely Updated')
        self.assertEqual(self.product1.price, 5000)
        self.assertEqual(self.product1.status, 'published')

    def test_complete_update_by_admin(self):
        """Admin can completely update any product"""
        self.client.force_authenticate(user=self.super_user)
        update_data = {
            'title_en': 'Admin Updated',
            'title_fa': 'بروزرسانی ادمین',
            'description': 'Admin description',
            'brief_description': 'Admin brief',
            'stock': 100,
            'price': 10000,
            'discount_percent': 0,
            'status': 'draft',
            'category': [self.category2.id],
            'user': self.admin_user.id
        }
        
        response = self.client.patch(self.url(self.product1.pk), update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.title_en, 'Admin Updated')
        self.assertEqual(self.product1.user, self.admin_user)
        self.assertEqual(list(self.product1.category.values_list('id', flat=True)), [self.category2.id])
