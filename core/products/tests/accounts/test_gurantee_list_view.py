from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from ...models import ProductGuarantee

User = get_user_model()

class ProductGuaranteeListViewTest(TestCase):
    
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
        
        # Create test guarantees
        self.guarantee1 = ProductGuarantee.objects.create(
            title_en='1 Year Warranty',
            title_fa='گارانتی ۱ ساله',
            slug='1-year-warranty',
            description='Basic coverage'
        )
        
        self.guarantee2 = ProductGuarantee.objects.create(
            title_en='2 Year Warranty',
            title_fa='گارانتی ۲ ساله',
            slug='2-year-warranty',
            description='Standard coverage'
        )
        
        self.guarantee3 = ProductGuarantee.objects.create(
            title_en='3 Year Warranty',
            title_fa='گارانتی ۳ ساله',
            slug='3-year-warranty',
            description='Premium coverage'
        )
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/guarantees_list.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:list_guarantee')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(response.status_code, 403)
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(response.status_code, 200)
    
    def test_queryset_returns_all_guarantees_by_default(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(len(response.context['guarantees']), 3)
        self.assertQuerySetEqual(
            response.context['guarantees'],
            [self.guarantee3, self.guarantee2, self.guarantee1],
            transform=lambda x: x
        )
    
    def test_search_functionality(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Search by English title
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'search': '2 Year'})
        self.assertEqual(len(response.context['guarantees']), 1)
        self.assertEqual(response.context['guarantees'][0], self.guarantee2)
        
        # Search by Farsi title
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'search': '۳ ساله'})
        self.assertEqual(len(response.context['guarantees']), 1)
        self.assertEqual(response.context['guarantees'][0], self.guarantee3)
        
        # Search by slug
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'search': '1-year'})
        self.assertEqual(len(response.context['guarantees']), 1)
        self.assertEqual(response.context['guarantees'][0], self.guarantee1)
        
        # Search with no results
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'search': 'nonexistent'})
        self.assertEqual(len(response.context['guarantees']), 0)
    
    def test_pagination(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create enough guarantees to test pagination
        for i in range(15):
            ProductGuarantee.objects.create(
                title_en=f'Warranty {i}',
                title_fa=f'گارانتی {i}',
                slug=f'warranty-{i}',
                description=f'Coverage {i}'
            )
        
        # First page should have 10 guarantees
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        self.assertEqual(len(response.context['guarantees']), 10)
        self.assertTrue(response.context['is_paginated'])
        
        # Second page should have the remaining 8 guarantees (3 original + 15 new - 10 on first page)
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'page': 2})
        self.assertEqual(len(response.context['guarantees']), 8)
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        
        self.assertEqual(response.context['search_query'], '')
        self.assertEqual(response.context['object_list'].count(), 3)
    
    def test_context_data_with_search(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:list_guarantee'), {'search': '3 year'})
        
        self.assertEqual(response.context['search_query'], '3 year')
        self.assertEqual(len(response.context['guarantees']), 1)
        self.assertEqual(response.context['guarantees'][0], self.guarantee3)
    
    def test_ordering(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        response = self.client.get(reverse('products:accounts:list_guarantee'))
        guarantees = response.context['guarantees']
        self.assertEqual(guarantees[0], self.guarantee3)
        self.assertEqual(guarantees[1], self.guarantee2)
        self.assertEqual(guarantees[2], self.guarantee1)