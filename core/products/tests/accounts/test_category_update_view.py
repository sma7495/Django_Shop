from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from ...models import ProductCategory
from ...accounts.forms import ProductCategoryForm

User = get_user_model()

class ProductCategoryUpdateViewTest(TestCase):
    
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
        
        # Create a test category to update
        self.category = ProductCategory.objects.create(
            title_en='Electronics',
            title_fa='الکترونیک',
            slug='electronics'
        )
        
        # Another category for testing duplicate slugs
        self.other_category = ProductCategory.objects.create(
            title_en='Clothing',
            title_fa='لباس',
            slug='clothing'
        )
        
        # Valid update data
        self.valid_data = {
            'title_en': 'Updated Electronics',
            'title_fa': 'الکترونیک بروزرسانی شده',
            'slug': 'updated-electronics',
        }
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_category.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk})}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_updates_category(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertRedirects(response, reverse('products:accounts:list_category'))
        self.category.refresh_from_db()
        self.assertEqual(self.category.title_en, 'Updated Electronics')
        self.assertEqual(self.category.title_fa, 'الکترونیک بروزرسانی شده')
        self.assertEqual(self.category.slug, 'updated-electronics')
        
        # Test success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'دسته‌بندی با موفقیت ویرایش شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.context['page_title'], "ویرایش دسته‌بندی")
        self.assertEqual(response.context['object'], self.category)
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Try to update category with existing slug
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = 'clothing'  # Same as other_category
        
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors
        self.category.refresh_from_db()
        self.assertEqual(self.category.slug, 'electronics')  # Slug shouldn't change

        
        # Test error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_missing_required_fields(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Missing title_en and title_fa
        invalid_data = {
            'slug': 'test-category',
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title_en, 'Electronics')  # Shouldn't change

        
        # Test error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Don't provide slug, should auto-generate from title_en
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Updated Category'
        
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.slug, 'updated-category')
    
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_category'))
    
    def test_partial_update(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Only update title_fa
        data = {
            'title_en': 'Electronics',  # Keep same
            'title_fa': 'الکترونیک جدید',
            'slug': 'electronics',  # Keep same
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_category', kwargs={'pk': self.category.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.title_en, 'Electronics')  # Unchanged
        self.assertEqual(self.category.title_fa, 'الکترونیک جدید')  # Updated
        self.assertEqual(self.category.slug, 'electronics')  # Unchanged