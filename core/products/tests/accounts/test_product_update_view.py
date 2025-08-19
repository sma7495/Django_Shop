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

User = get_user_model()
# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductUpdateViewTest(TestCase):
    
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
        
        # Create a test product to update
        self.product = Product.objects.create(
            title_en='Original Product',
            title_fa='محصول اصلی',
            description='Original description',
            brief_description='Original brief description',
            price=1000,
            discount_percent=5,
            slug='original-product',
            stock=10,
            status='published',
            user=self.superuser,
        )
        self.product.category.add(self.category)
        self.product.color.add(self.color)
        self.product.guarantee = self.guarantee
        self.product.save()
        
        # Add some existing images and specifications
        self.image1 = ProductImage.objects.create(
            product=self.product,
            image=self.create_test_image()
        )
        self.image2 = ProductImage.objects.create(
            product=self.product,
            image=self.create_test_image()
        )
        
        self.spec1 = ProductSpecifications.objects.create(
            product=self.product,
            title_en='Weight',
            title_fa='وزن',
            value='1kg'
        )
        self.spec2 = ProductSpecifications.objects.create(
            product=self.product,
            title_en='Color',
            title_fa='رنگ',
            value='Red'
        )
        
        # Update data
        self.update_data = {
            'title_en': 'Updated Product',
            'title_fa': 'محصول بروزرسانی شده',
            'description': 'Updated description',
            'brief_description': 'Updated brief description',
            'price': 1500,
            'discount_percent': 10,
            'slug': 'updated-product',
            'stock': 15,
            'status': 'draft',
            'category': [str(self.category.id)],
            'color': [str(self.color.id)],
            'guarantee': str(self.guarantee.id),
            # Existing specs updates
            f'existing_spec_title_en_{self.spec1.id}': 'Updated Weight',
            f'existing_spec_title_fa_{self.spec1.id}': 'وزن بروزرسانی شده',
            f'existing_spec_value_{self.spec1.id}': '2kg',
            f'existing_spec_title_en_{self.spec2.id}': 'Updated Color',
            f'existing_spec_title_fa_{self.spec2.id}': 'رنگ بروزرسانی شده',
            f'existing_spec_value_{self.spec2.id}': 'Blue',
            # New specs
            'new_spec_title_en[]': ['Size'],
            'new_spec_title_fa[]': ['سایز'],
            'new_spec_value[]': ['Large'],
        }
        
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
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_new.html')
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        self.assertRedirects(
            response,
            f"{reverse('account:login')}?next={reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk})}"
        )
    
    def test_view_requires_admin_or_superuser(self):
        # Test with regular user
        self.client.login(email='regular@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test with staff user
        self.client.login(email='staff@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test with superuser
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_form_valid_updates_product(self):
        self.client.login(email='admin@example.com', password='testpass123')
        data = self.update_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.product.refresh_from_db()
        self.assertEqual(self.product.title_en, 'Updated Product')
        self.assertEqual(self.product.title_fa, 'محصول بروزرسانی شده')
        self.assertEqual(self.product.price, 1500)
        self.assertEqual(self.product.status, 'draft')
    
    def test_additional_images_deletion(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Request to delete one of the additional images
        data = self.update_data.copy()
        data['delete_images'] = [str(self.image1.id)]
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductImage.objects.filter(product=self.product).count(), 1)
        self.assertFalse(ProductImage.objects.filter(id=self.image1.id).exists())
    
    def test_new_additional_images_upload(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.update_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        
        # Create test images
        images = [self.create_test_image() for _ in range(2)]
        data['additional_images'] = images
        files = {'image': image_file, 'additional_images' : images}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )

        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductImage.objects.filter(product=self.product).count(), 4)  # 2 existing + 2 new
    
    def test_additional_images_limit(self):
        self.client.login(email='admin@example.com', password='testpass123')
        data = self.update_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        
        # Create test images
        images = [self.create_test_image() for _ in range(7)] # only 5 images saved
        data['additional_images'] = images
        files = {'image': image_file, 'additional_images' : images}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductImage.objects.filter(product=self.product).count(), 7)  # 5 new + 2 old
    
    def test_specifications_updates(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.update_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.spec1.refresh_from_db()
        self.spec2.refresh_from_db()
        
        self.assertEqual(self.spec1.title_en, 'Updated Weight')
        self.assertEqual(self.spec1.title_fa, 'وزن بروزرسانی شده')
        self.assertEqual(self.spec1.value, '2kg')
        
        self.assertEqual(self.spec2.title_en, 'Updated Color')
        self.assertEqual(self.spec2.title_fa, 'رنگ بروزرسانی شده')
        self.assertEqual(self.spec2.value, 'Blue')
    
    def test_specifications_deletion(self):
        self.client.login(email='admin@example.com', password='testpass123')
        data = self.update_data.copy()
        
        data['delete_specs'] = [str(self.spec1.id)]

        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductSpecifications.objects.filter(product=self.product).count(), 2)  # 1 deleted + 1 existing + 1 new
        self.assertFalse(ProductSpecifications.objects.filter(id=self.spec1.id).exists())
    
    def test_new_specifications_creation(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        data = self.update_data.copy()
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductSpecifications.objects.filter(product=self.product).count(), 3)  # 2 existing + 1 new
        
        new_spec = ProductSpecifications.objects.get(title_en='Size')
        self.assertEqual(new_spec.title_fa, 'سایز')
        self.assertEqual(new_spec.value, 'Large')
    
    def test_empty_specifications_deletion(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Make one specification empty
        data = self.update_data.copy()
        data[f'existing_spec_title_en_{self.spec1.id}'] = ''
        data[f'existing_spec_title_fa_{self.spec1.id}'] = ''
        data[f'existing_spec_value_{self.spec1.id}'] = ''
        
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        files = {'image': image_file}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductSpecifications.objects.filter(product=self.product).count(), 2)  # 1 deleted (empty) + 1 existing + 1 new
        self.assertFalse(ProductSpecifications.objects.filter(id=self.spec1.id).exists())
    
    def test_success_message_with_images(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Delete one image and add two new ones
        images = [self.create_test_image() for _ in range(2)]
        data = self.update_data.copy()
        data['delete_images'] = [str(self.image1.id)]
        data['additional_images'] = images
        
        data['user'] = self.superuser.id

        image_file = self.create_test_image()
        data['image'] = image_file
        
        files = {'image': image_file, 'additional_images': images}  # Create separate files dictionary

        # Test the client post
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=data,
            files=files,  # Pass files separately
            format='multipart'
        )

        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("محصول «محصول بروزرسانی شده» با موفقیت ویرایش شد.", str(messages[0]))
        self.assertIn("1 تصویر حذف شد", str(messages[0]))
        self.assertIn("2 تصویر اضافه شد", str(messages[0]))
    
    def test_context_data(self):
        self.client.login(email='admin@example.com', password='testpass123')
        response = self.client.get(reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}))
        
        self.assertEqual(response.context['page_title'], "ویرایش محصول")
        self.assertTrue(response.context['editing'])
        self.assertEqual(list(response.context['existing_images']), [self.image2, self.image1])  # Ordered by -created_date
        self.assertFalse(response.context['has_main_image'])  # We didn't set a main image in setUp
    
    def test_invalid_form_submission(self):
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Missing required fields
        invalid_data = {
            'title_en': '',  # Required field
            'title_fa': '',  # Required field
            'price': 'not a number',  # Invalid number
        }
        
        response = self.client.post(
            reverse('products:accounts:edit_product', kwargs={'pk': self.product.pk}),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)  # Should re-render form
        self.product.refresh_from_db()
        self.assertEqual(self.product.title_en, 'Original Product')  # Should not be updated