from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from ...models import ProductColor
from ...accounts.forms import ProductColorForm

User = get_user_model()

class ProductColorUpdateViewTest(TestCase):
    
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
        
        # Create test color to update
        self.color = ProductColor.objects.create(
            title_en='Red',
            title_fa='قرمز',
            slug='red'
        )
        
        # Another color for testing duplicate slugs
        self.other_color = ProductColor.objects.create(
            title_en='Blue',
            title_fa='آبی',
            slug='blue'
        )
        
        # Valid update data
        self.valid_data = {
            'title_en': 'Dark Red',
            'title_fa': 'قرمز تیره',
            'slug': 'dark-red',
        }
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_color.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk})}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertEqual(response.status_code, 403)
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_updates_color(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products:accounts:list_color'))
        self.color.refresh_from_db()
        self.assertEqual(self.color.title_en, 'Dark Red')
        self.assertEqual(self.color.title_fa, 'قرمز تیره')
        self.assertEqual(self.color.slug, 'dark-red')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'رنگ با موفقیت ویرایش شد.')
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}))
        self.assertEqual(response.context['page_title'], "ویرایش رنگ")
        self.assertEqual(response.context['object'], self.color)
    
    def test_duplicate_slug_validation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        duplicate_data = self.valid_data.copy()
        duplicate_data['slug'] = 'blue'
        
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=duplicate_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.color.refresh_from_db()
        self.assertEqual(self.color.slug, 'red')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_missing_required_fields(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        invalid_data = {'slug': 'test-color'}
        
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)
        self.color.refresh_from_db()
        self.assertEqual(self.color.title_en, 'Red')
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')
    
    def test_auto_generated_slug(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.valid_data.copy()
        del data['slug']
        data['title_en'] = 'Updated Color'
        
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.color.refresh_from_db()
        self.assertEqual(self.color.slug, 'updated-color')
    
    def test_get_success_url(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=self.valid_data
        )
        self.assertRedirects(response, reverse('products:accounts:list_color'))
    
    def test_partial_update(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = {
            'title_en': 'Red',
            'title_fa': 'قرمز جدید',
            'slug': 'red',
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_color', kwargs={'pk': self.color.pk}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.color.refresh_from_db()
        self.assertEqual(self.color.title_en, 'Red')
        self.assertEqual(self.color.title_fa, 'قرمز جدید')
        self.assertEqual(self.color.slug, 'red')