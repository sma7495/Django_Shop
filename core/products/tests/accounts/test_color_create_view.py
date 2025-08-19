from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from ...models import ProductColor
from ...accounts.forms import ProductColorForm

User = get_user_model()

class ProductColorCreateViewTest(TestCase):
    
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
            'title_en': 'Red',
            'title_fa': 'قرمز',
            'slug': 'red',
        }
        
        # Existing color to test duplicate slugs
        self.existing_color = ProductColor.objects.create(
            title_en='Blue',
            title_fa='آبی',
            slug='blue'
        )
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_color.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:add_color')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_creates_color(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_color'),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products:accounts:list_color'))
        self.assertEqual(ProductColor.objects.count(), 2)
        new_color = ProductColor.objects.get(slug='red')
        self.assertEqual(new_color.title_en, 'Red')
        self.assertEqual(new_color.title_fa, 'قرمز')
        
        # Test success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'رنگ جدید با موفقیت ایجاد شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_color'))
        self.assertEqual(response.context['page_title'], "افزودن رنگ جدید")
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = 'blue'
        
        response = self.client.post(
            reverse('products:accounts:add_color'),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductColor.objects.count(), 1)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_missing_required_fields(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        invalid_data = {'slug': 'test-color'}
        
        response = self.client.post(
            reverse('products:accounts:add_color'),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductColor.objects.count(), 1)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Test Color'
        
        response = self.client.post(
            reverse('products:accounts:add_color'),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductColor.objects.count(), 2)
        new_color = ProductColor.objects.get(title_en='Test Color')
        self.assertEqual(new_color.slug, 'test-color')
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_color'),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_color'))