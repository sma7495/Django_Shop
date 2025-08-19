from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import shutil
from django.test import TestCase, override_settings
import os
from django.conf import settings


from ...models import Product, ProductImage, ProductSpecifications, ProductCategory, ProductColor, ProductGuarantee
from ...accounts.forms import ProductForm
from ...accounts.permissions import AdminOrSuperuserRequiredMixin
from ...accounts.views import ProductCreateView

User = get_user_model()

# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductCreateViewTest(TestCase):
    
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
            is_active = True,
            type = 2 # type = admin
            
        )
        self.regular_user = User.objects.create_user(
            email='regular@example.com',
            password='testpass123',
            is_active = True,

        )
        
        # Set up the factory for request creation
        self.factory = RequestFactory()
        # # In your test:
        # self.image = SimpleUploadedFile(
        #     name='test_image.jpg',
        #     content=create_test_image().read(),
        #     content_type='image/jpeg'
        # )
        
        # Create related model instances
        self.category = ProductCategory.objects.create(
            title_en='Test Category',
            title_fa='دسته‌بندی تستی',
            slug='test-category'
        )
        
        self.color = ProductColor.objects.create(
            title_en='Red',
            title_fa='قرمز'
        )
        
        self.guarantee = ProductGuarantee.objects.create(
            title_en='2 Year Warranty',
            title_fa='گارانتی ۲ ساله',
        )
        
        # Update valid_data to use the actual objects
        self.image_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_image.jpg')
        
        self.valid_data = {
            'title_en': 'Test Product1002535',
            'title_fa': 'محصول تستی',
            'description': 'Test description',
            'brief_description': 'Brief test description',
            'price': 1000,  # Price in Rials
            'discount_percent': 10,
            'slug': 'test_for_products_accounts_ProductCreateView',
            'stock': 10,
            'status': 'published',
            'category': [str(self.category.id)],  # Use the created category's ID
            'color': [str(self.color.id)],  # Use the created color's ID
            'guarantee': str(self.guarantee.id),  # Use the created guarantee's ID
            # Specifications data
            'new_spec_title_en[]': ['Weight', 'Color'],
            'new_spec_title_fa[]': ['وزن', 'رنگ'],
            'new_spec_value[]': ['1kg', 'Red'],
        }
        # # In your test setup:
        # self.valid_data_with_image = {
        #     **self.valid_data,
        #     'image': self.image  # The SimpleUploadedFile you created
        # }
    def tearDown(self):
        # Clean up the test media directory
        try:
            shutil.rmtree(TEST_MEDIA_ROOT)
        except FileNotFoundError:
            pass    

    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile('test.jpg', file.getvalue(), 'image/jpeg')
    
    def test_view_uses_correct_template(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_new.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:add_product')}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_creates_product(self):
        self.client.login(email='admin@example.com', password='testpass123')
        # In your test method
        data = self.valid_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        #     # Print form errors if any
        # if hasattr(response, 'context') and 'form' in response.context:
        #     print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.title_en, 'Test Product1002535')
        self.assertEqual(product.user, self.superuser)
        
    def test_form_valid_with_additional_images(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create multiple test images
        images = [
            self.create_test_image()for i in range(3)
        ]
        data = self.valid_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        data['additional_images'] = images
        files = {'image': image_file, 'additional_images': images}  # Create separate files dictionary
        
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=data,
            files=files
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductImage.objects.count(), 3)
        self.assertEqual(ProductImage.objects.filter(product__title_en='Test Product1002535').count(), 3)
    
    def test_form_valid_with_specifications(self):
        self.client.login(email='admin@example.com', password='testpass123')
        # In your test method
        data = self.valid_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductSpecifications.objects.count(), 2)
        specs = ProductSpecifications.objects.filter(product__title_en='Test Product1002535').order_by('-title_en')

        self.assertEqual(specs[0].title_en, 'Weight')
        self.assertEqual(specs[0].title_fa, 'وزن')
        self.assertEqual(specs[0].value, '1kg')
        self.assertEqual(specs[1].title_en, 'Color')
        self.assertEqual(specs[1].title_fa, 'رنگ')
        self.assertEqual(specs[1].value, 'Red')
    
    def test_form_valid_limits_to_5_images(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create multiple test images
        images = [
            self.create_test_image()for i in range(7)
        ]
        data = self.valid_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        data['additional_images'] = images
        files = {'image': image_file, 'additional_images': images}  # Create separate files dictionary
        
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=data,
            files=files
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductImage.objects.count(), 5)  # Should be limited to 5
    
    def test_success_message(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Create multiple test images
        images = [
            self.create_test_image()for i in range(3)
        ]
        data = self.valid_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        data['additional_images'] = images
        files = {'image': image_file, 'additional_images': images}  # Create separate files dictionary
        
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=data,
            files=files
        )
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "محصول «محصول تستی» با 3 تصویر اضافی و 2 مشخصه اضافه شد.",
            str(messages[0])
        )
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:add_product'))
        self.assertEqual(response.context['page_title'], "افزودن محصول جدید")
    
    def test_invalid_form_submission(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Missing required fields
        invalid_data = {
            'title_en': '',  # Required field
            'title_fa': '',  # Required field
            'price': 'not a number',  # Invalid number
        }
        
        response = self.client.post(
            reverse('products:accounts:add_product'),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)  # Should re-render form
        # self.assertFormError(response, 'form', 'title_en', 'This field is required.')
        # self.assertFormError(response, 'form', 'title_fa', 'This field is required.')
        # self.assertFormError(response, 'form', 'price', 'Enter a number.')
        self.assertEqual(Product.objects.count(), 0)  # No product should be created