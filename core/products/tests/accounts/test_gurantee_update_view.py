from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from ...models import ProductGuarantee
from ...accounts.forms import ProductGuaranteeForm

User = get_user_model()

class ProductGuaranteeUpdateViewTest(TestCase):
    
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
        
        # Create test guarantee to update
        self.guarantee = ProductGuarantee.objects.create(
            title_en='1 Year Warranty',
            title_fa='گارانتی ۱ ساله',
            slug='1-year-warranty',
            description='Basic coverage'
        )
        
        # Another guarantee for testing duplicate slugs
        self.other_guarantee = ProductGuarantee.objects.create(
            title_en='3 Year Warranty',
            title_fa='گارانتی ۳ ساله',
            slug='3-year-warranty',
            description='Premium coverage'
        )
        
        # Valid update data
        self.valid_data = {
            'title_en': 'Extended Warranty',
            'title_fa': 'گارانتی تمدید شده',
            'slug': 'extended-warranty',
            'description': 'Extended coverage details'
        }
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_guarantee.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk})}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertEqual(response.status_code, 403)
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_updates_guarantee(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products:accounts:list_guarantee'))
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.title_en, 'Extended Warranty')
        self.assertEqual(self.guarantee.title_fa, 'گارانتی تمدید شده')
        self.assertEqual(self.guarantee.slug, 'extended-warranty')
        self.assertEqual(self.guarantee.description, 'Extended coverage details')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'گارانتی با موفقیت ویرایش شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}))
        self.assertEqual(response.context['page_title'], "ویرایش گارانتی")
        self.assertEqual(response.context['object'], self.guarantee)
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = '3-year-warranty'
        
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.slug, '1-year-warranty')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_missing_required_fields(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        invalid_data = {
            'slug': 'test-guarantee',
            'description': 'Test description'
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.title_en, '1 Year Warranty')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Updated Guarantee'
        
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.slug, 'updated-guarantee')
    
    def test_description_field_update(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        data['description'] = 'New updated description'
        
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.description, 'New updated description')
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_guarantee'))
    
    def test_partial_update(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = {
            'title_en': '1 Year Warranty',
            'title_fa': 'گارانتی ۱ ساله',
            'slug': '1-year-warranty',
            'description': 'Updated coverage details'
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_guarantee', kwargs={'pk': self.guarantee.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.guarantee.refresh_from_db()
        self.assertEqual(self.guarantee.title_en, '1 Year Warranty')
        self.assertEqual(self.guarantee.description, 'Updated coverage details')