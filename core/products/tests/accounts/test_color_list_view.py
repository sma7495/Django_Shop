from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from ...models import ProductColor

User = get_user_model()

class ProductColorListViewTest(TestCase):
    
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
        
        # Create test colors
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
        
        self.color3 = ProductColor.objects.create(
            title_en='Green',
            title_fa='سبز',
            slug='green'
        )
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/color_list.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:list_color')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(response.status_code, 403)
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(response.status_code, 200)
    
    def test_queryset_returns_all_colors_by_default(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(len(response.context['colors']), 3)
        self.assertQuerySetEqual(
            response.context['colors'],
            [self.color3, self.color2, self.color1],
            transform=lambda x: x
        )
    
    def test_search_functionality(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Search by English title
        response = self.client.get(reverse('products:accounts:list_color'), {'search': 'Red'})
        self.assertEqual(len(response.context['colors']), 1)
        self.assertEqual(response.context['colors'][0], self.color1)
        
        # Search by Farsi title
        response = self.client.get(reverse('products:accounts:list_color'), {'search': 'قرمز'})
        self.assertEqual(len(response.context['colors']), 1)
        self.assertEqual(response.context['colors'][0], self.color1)
        
        # Search by slug
        response = self.client.get(reverse('products:accounts:list_color'), {'search': 'blu'})
        self.assertEqual(len(response.context['colors']), 1)
        self.assertEqual(response.context['colors'][0], self.color2)
        
        # Search with no results
        response = self.client.get(reverse('products:accounts:list_color'), {'search': 'nonexistent'})
        self.assertEqual(len(response.context['colors']), 0)
    
    def test_pagination(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create enough colors to test pagination
        for i in range(15):
            ProductColor.objects.create(
                title_en=f'Color {i}',
                title_fa=f'رنگ {i}',
                slug=f'color-{i}'
            )
        
        # First page should have 10 colors
        response = self.client.get(reverse('products:accounts:list_color'))
        self.assertEqual(len(response.context['colors']), 10)
        self.assertTrue(response.context['is_paginated'])
        
        # Second page should have the remaining 8 colors (3 original + 15 new - 10 on first page)
        response = self.client.get(reverse('products:accounts:list_color'), {'page': 2})
        self.assertEqual(len(response.context['colors']), 8)
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'))
        
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['object_list'].count(), 3)
    
    def test_context_data_with_search(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_color'), {'search': 'green'})
        
        self.assertEqual(response.context['search_query'], 'green')
        self.assertEqual(len(response.context['colors']), 1)
        self.assertEqual(response.context['colors'][0], self.color3)
    
    def test_ordering(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        response = self.client.get(reverse('products:accounts:list_color'))
        colors = response.context['colors']
        self.assertEqual(colors[0], self.color3)
        self.assertEqual(colors[1], self.color2)
        self.assertEqual(colors[2], self.color1)