from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from ...models import ProductGuarantee
from ...accounts.forms import ProductGuaranteeForm

User = get_user_model()

class ProductGuaranteeCreateViewTest(TestCase):
    
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
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
        
        # Valid form data
        self.valid_data = {
            'title_en': '2 Year Warranty',
            'title_fa': 'گارانتی ۲ ساله',
            'slug': '2-year-warranty',
            'description': 'Full coverage for 2 years'
        }
        
        # Existing guarantee to test duplicate slugs
        self.existing_guarantee = ProductGuarantee.objects.create(
            title_en='1 Year Warranty',
            title_fa='گارانتی ۱ ساله',
            slug='1-year-warranty',
            description='Basic coverage'
        )
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_guarantee.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:add_guarantee')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertEqual(response.status_code, 403)
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_creates_guarantee(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_guarantee'),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products:accounts:list_guarantee'))
        self.assertEqual(ProductGuarantee.objects.count(), 2)
        new_guarantee = ProductGuarantee.objects.get(slug='2-year-warranty')
        self.assertEqual(new_guarantee.title_en, '2 Year Warranty')
        self.assertEqual(new_guarantee.title_fa, 'گارانتی ۲ ساله')
        self.assertEqual(new_guarantee.description, 'Full coverage for 2 years')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'گارانتی جدید با موفقیت ایجاد شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_guarantee'))
        self.assertEqual(response.context['page_title'], "افزودن گارانتی جدید")
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = '1-year-warranty'
        
        response = self.client.post(
            reverse('products:accounts:add_guarantee'),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductGuarantee.objects.count(), 1)
        
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
            reverse('products:accounts:add_guarantee'),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductGuarantee.objects.count(), 1)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Test Guarantee'
        
        response = self.client.post(
            reverse('products:accounts:add_guarantee'),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductGuarantee.objects.count(), 2)
        new_guarantee = ProductGuarantee.objects.get(title_en='Test Guarantee')
        self.assertEqual(new_guarantee.slug, 'test-guarantee')
    
    def test_description_field(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        data['description'] = 'Extended coverage description'
        
        response = self.client.post(
            reverse('products:accounts:add_guarantee'),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        new_guarantee = ProductGuarantee.objects.get(slug='2-year-warranty')
        self.assertEqual(new_guarantee.description, 'Extended coverage description')
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_guarantee'),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_guarantee'))