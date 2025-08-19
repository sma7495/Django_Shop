from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import ProductCategory
from ...accounts.forms import ProductCategoryForm

User = get_user_model()

class ProductCategoryCreateViewTest(TestCase):
    
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
            'title_en': 'Electronics',
            'title_fa': 'الکترونیک',
            'slug': 'electronics',
        }
        
        # Existing category to test duplicate slugs
        self.existing_category = ProductCategory.objects.create(
            title_en='Clothing',
            title_fa='لباس',
            slug='clothing'
        )
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_category.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:add_category')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_creates_category(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertRedirects(response, reverse('products:accounts:list_category'))
        self.assertEqual(ProductCategory.objects.count(), 2)  # Existing + new
        new_category = ProductCategory.objects.get(slug='electronics')
        self.assertEqual(new_category.title_en, 'Electronics')
        self.assertEqual(new_category.title_fa, 'الکترونیک')

        
        # Test success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'دسته‌بندی جدید با موفقیت ایجاد شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_category'))
        self.assertEqual(response.context['page_title'], "افزودن دسته‌بندی جدید")
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Try to create category with existing slug
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = 'clothing'  # Same as existing_category
        
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors
        self.assertEqual(ProductCategory.objects.count(), 1)  # Only existing remains
        
        # Test error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_missing_required_fields(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Missing title_en and title_fa
        invalid_data = {
            'slug': 'test-category',
            'is_active': True
        }
        
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductCategory.objects.count(), 1)  # Only existing remains
        
        # Test error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Don't provide slug, should auto-generate from title_en
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Test Category'
        
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductCategory.objects.count(), 2)
        new_category = ProductCategory.objects.get(title_en='Test Category')
        self.assertEqual(new_category.slug, 'test-category')
    
    def test_inactive_category_creation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create inactive category
        data = self.valid_data.copy()
        data['is_active'] = False
        
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        new_category = ProductCategory.objects.get(slug='electronics')
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:add_category'),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_category'))