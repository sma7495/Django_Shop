from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.test import TestCase, override_settings, RequestFactory
import os
from django.conf import settings
import shutil


from ...models import Product, ProductVideos
from ...accounts.forms import ProductVideosForm
from ...accounts.views import ProductVideoUpdateView
from ...accounts.permissions import AdminOrSuperuserRequiredMixin

User = get_user_model()

# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductVideoUpdateViewTest(TestCase):
    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'JPEG')
        file.seek(0)
        return SimpleUploadedFile('test.jpg', file.getvalue(), 'image/jpeg')
    
    def setUp(self):
        # Create test users
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
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
        
        # Create test product
        self.product = Product.objects.create(
            title_en='Laptop',
            title_fa='لپ تاپ',
            description='Gaming laptop',
            price=2000,
            discount_percent=15,
            slug='laptop',
            status='draft',
            user=self.superuser,
            image=self.create_test_image(),
        )
        
        # Create test video
        self.test_video = ProductVideos.objects.create(
            user=self.admin_user,
            title_en='Original Video',
            title_fa='ویدیو اصلی',
            slug='original-video',
            video_url='https://example.com/original',
            description='Original description',
            cover = self.create_test_image()
        )
        self.test_video.product.add(self.product)
        
        # Test image file
        self.test_image = self.create_test_image()
        
        # Form data for updates
        self.valid_update_data = {
            'user': self.admin_user.id,
            'product': [self.product.id],
            'title_en': 'Updated Video',
            'title_fa': 'ویدیو به روز شده',
            'slug': 'updated-video',
            'cover': self.test_image,
            'video_url': 'https://example.com/updated',
            'description': 'Updated description'
        }
        
        self.factory = RequestFactory()
        self.url = reverse('products:accounts:edit_video', kwargs={'pk': self.test_video.pk})
        self.success_url = reverse('products:accounts:list_video')
        
    def tearDown(self):
        # Clean up the test media directory
        try:
            shutil.rmtree(TEST_MEDIA_ROOT)
        except FileNotFoundError:
            pass   
        
    def test_view_uses_correct_template(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/products/add_video.html')

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_view_requires_admin_or_superuser(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_view_accessible_to_admin_users(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_has_correct_context(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.context['page_title'], "ویرایش فیلم")
        self.assertEqual(response.context['object'], self.test_video)

    def test_form_valid_updates_video(self):
        self.client.force_login(self.admin_user)
        files = {'cover': self.test_image}
        response = self.client.post(
            self.url, 
            data=self.valid_update_data, 
            files=files, 
            format='multipart', 
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.test_video.refresh_from_db()
        
        # Check updated fields
        self.assertEqual(self.test_video.title_en, 'Updated Video')
        self.assertEqual(self.test_video.title_fa, 'ویدیو به روز شده')
        self.assertEqual(self.test_video.slug, 'updated-video')
        self.assertEqual(self.test_video.video_url, 'https://example.com/updated')
        self.assertEqual(self.test_video.description, 'Updated description')
        self.assertTrue(self.product in self.test_video.product.all())

    def test_success_message_on_update(self):
        self.client.force_login(self.admin_user)
        files = {'cover': self.test_image}
        response = self.client.post(
            self.url, 
            data=self.valid_update_data, 
            files=files, 
            format='multipart', 
            follow=True
        )
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'فیلم با موفقیت ویرایش شد.')

    def test_invalid_form_shows_errors(self):
        self.client.force_login(self.admin_user)
        invalid_data = self.valid_update_data.copy()
        invalid_data['title_en'] = 'فارسی'  # Make it invalid
        files = {'cover': self.test_image}
        response = self.client.post(
            self.url, 
            data=invalid_data, 
            files=files, 
            format='multipart', 
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')

    def test_success_url_redirect(self):
        self.client.force_login(self.admin_user)
        files = {'cover': self.test_image}
        response = self.client.post(
            self.url, 
            data=self.valid_update_data, 
            files=files, 
            format='multipart'
        )
        self.assertRedirects(response, self.success_url)

    def test_form_class_used(self):
        view = ProductVideoUpdateView()
        self.assertEqual(view.form_class, ProductVideosForm)

    def test_model_used(self):
        view = ProductVideoUpdateView()
        self.assertEqual(view.model, ProductVideos)

