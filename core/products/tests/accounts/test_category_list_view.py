from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from ...models import ProductCategory

User = get_user_model()

class ProductCategoryListViewTest(TestCase):
    
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
        
        # Create test categories
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
        
        self.category3 = ProductCategory.objects.create(
            title_en='Books',
            title_fa='کتاب',
            slug='books'
        )
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/category_list.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:list_category')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(response.status_code, 200)
    
    def test_queryset_returns_all_categories_by_default(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(len(response.context['categories']), 3)
        self.assertQuerySetEqual(
            response.context['categories'],
            [self.category3, self.category2, self.category1],  # Default ordering is by -id
            transform=lambda x: x
        )
    
    def test_search_functionality(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Search by English title
        response = self.client.get(reverse('products:accounts:list_category'), {'search': 'Electronics'})
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(response.context['categories'][0], self.category1)
        
        # Search by Farsi title
        response = self.client.get(reverse('products:accounts:list_category'), {'search': 'الکترونیک'})
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(response.context['categories'][0], self.category1)
        
        # Search by slug
        response = self.client.get(reverse('products:accounts:list_category'), {'search': 'cloth'})
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(response.context['categories'][0], self.category2)
        
        # Search with no results
        response = self.client.get(reverse('products:accounts:list_category'), {'search': 'nonexistent'})
        self.assertEqual(len(response.context['categories']), 0)
    
    def test_pagination(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create enough categories to test pagination
        for i in range(15):
            ProductCategory.objects.create(
                title_en=f'Category {i}',
                title_fa=f'دسته‌بندی {i}',
                slug=f'category-{i}'
            )
        
        # First page should have 10 categories
        response = self.client.get(reverse('products:accounts:list_category'))
        self.assertEqual(len(response.context['categories']), 10)
        self.assertTrue(response.context['is_paginated'])
        
        # Second page should have the remaining 8 categories (3 original + 15 new - 10 on first page)
        response = self.client.get(reverse('products:accounts:list_category'), {'page': 2})
        self.assertEqual(len(response.context['categories']), 8)
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'))
        
        # Test context variables
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['object_list'].count(), 3)
    
    def test_context_data_with_search(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_category'), {'search': 'book'})
        
        # Test context variables with search
        self.assertEqual(response.context['search_query'], 'book')
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(response.context['categories'][0], self.category3)
    
    def test_ordering(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Test default ordering (should be by -id)
        response = self.client.get(reverse('products:accounts:list_category'))
        categories = response.context['categories']
        self.assertEqual(categories[0], self.category3)  # Most recently created
        self.assertEqual(categories[1], self.category2)
        self.assertEqual(categories[2], self.category1)  # Oldest