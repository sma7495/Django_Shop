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
from ...accounts.views import ProductVideoCreateView
from ...accounts.permissions import AdminOrSuperuserRequiredMixin

User = get_user_model()

# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductVideoCreateViewTest(TestCase):
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
            is_active = True,
            type = 2 # type = admin
            
        )
        self.regular_user = User.objects.create_user(
            email='regular@example.com',
            password='testpass123',
            is_active = True,

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
            image = self.create_test_image(),

        )
        
        # Test image file
        self.test_image = self.create_test_image()
        
        # Form data
        self.valid_form_data = {
            'user': self.admin_user.id,
            'product': [self.product.id],
            'title_en': 'Test Video',
            'title_fa': 'تست ویدیو',
            'slug': 'test-video',
            'cover': self.test_image,
            'video_url': 'https://example.com/video',
            'description': 'Test description'
        }
        
        self.factory = RequestFactory()
        self.url = reverse('products:accounts:add_video')
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
        self.assertEqual(response.context['page_title'], "افزودن فیلم جدید")

    def test_form_valid_creates_video(self):
        self.client.force_login(self.admin_user)
        files={'cover': self.test_image}
        response = self.client.post(self.url, data=self.valid_form_data, files=files, format='multipart', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductVideos.objects.count(), 1)
        
        video = ProductVideos.objects.first()
        self.assertEqual(video.title_en, 'Test Video')
        self.assertEqual(video.title_fa, 'تست ویدیو')
        self.assertEqual(video.user, self.admin_user)
        self.assertTrue(self.product in video.product.all())

    def test_success_message_on_creation(self):
        self.client.force_login(self.admin_user)
        
        files={'cover': self.test_image}
        response = self.client.post(self.url, data=self.valid_form_data, files=files, format='multipart', follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'فیلم جدید با موفقیت ایجاد شد.')

    def test_invalid_form_shows_errors(self):
        self.client.force_login(self.admin_user)
        invalid_data = self.valid_form_data.copy()
        invalid_data['title_en'] = 'فارسی'  # Make it invalid
        files={'cover': self.test_image}
        response = self.client.post(self.url, data=invalid_data, files=files, format='multipart', follow=True)
        
        self.assertEqual(response.status_code, 200)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'لطفاً خطاهای زیر را اصلاح کنید.')

    def test_success_url_redirect(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url, data=self.valid_form_data)
        
        self.assertRedirects(response, self.success_url)

    def test_form_class_used(self):
        view = ProductVideoCreateView()
        self.assertEqual(view.form_class, ProductVideosForm)

    def test_model_used(self):
        view = ProductVideoCreateView()
        self.assertEqual(view.model, ProductVideos)
