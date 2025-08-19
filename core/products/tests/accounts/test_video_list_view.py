from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
import datetime
from io import BytesIO
from PIL import Image
from django.test import TestCase, override_settings, RequestFactory
import os
from django.conf import settings
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Product, ProductVideos
from ...accounts.views import ProductVideoListView

User = get_user_model()

# Create a temp directory for test media
TEST_MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/tests')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductVideoListViewTest(TestCase):
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
        self.product1 = Product.objects.create(
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
        
        self.product2 = Product.objects.create(
            title_en='Phone',
            title_fa='موبایل',
            slug='phone',
            description='Gaming laptop',
            price=2000,
            discount_percent=15,
            status='draft',
            user=self.superuser,
            image=self.create_test_image(),
        )
        
        # Create test videos with different attributes
        now = timezone.now()
        
        # Video with cover and both titles
        self.video1 = ProductVideos.objects.create(
            user=self.admin_user,
            title_en='Video 1',
            title_fa='ویدیو ۱',
            slug='video-1',
            video_url='https://example.com/1',
            description='Description 1',
            cover=self.create_test_image(),
            created_date=now - datetime.timedelta(days=3)
            
        )
        self.video1.product.add(self.product1)
        
        # Video without cover and only Persian title
        self.video2 = ProductVideos.objects.create(
            user=self.admin_user,
            title_fa='ویدیو ۲',
            slug='video-2',
            video_url='https://example.com/2',
            description='Description 2',
            created_date=now - datetime.timedelta(days=2)
        )
        self.video2.product.add(self.product2)
        
        # Video with cover and only English title
        self.video3 = ProductVideos.objects.create(
            user=self.superuser,
            title_en='Video 3',
            slug='video-3',
            video_url='https://example.com/3',
            description='Description 3',
            cover=self.create_test_image(),
            created_date=now - datetime.timedelta(days=1)
        )
        self.video3.product.add(self.product1, self.product2)
        
        self.url = reverse('products:accounts:list_video')
        self.factory = RequestFactory()

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
        self.assertTemplateUsed(response, 'accounts/products/video_list.html')
    
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
    
    def test_context_contains_videos(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['videos']), 3)
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video2, response.context['videos'])
        self.assertIn(self.video3, response.context['videos'])
    
    def test_pagination(self):
        # Create enough videos to trigger pagination
        for i in range(15):
            ProductVideos.objects.create(
                user=self.admin_user,
                title_en=f'Video {i+4}',
                slug=f'video-{i+4}',
                video_url=f'https://example.com/{i+4}',
                cover = self.create_test_image(),
            )
        
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['videos']), 10)  # Default pagination
        self.assertTrue(response.context['is_paginated'])
    
    def test_search_filter(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {'search': 'ویدیو'})
        self.assertEqual(len(response.context['videos']), 2)  # video1 and video2 have Persian titles
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video2, response.context['videos'])
        self.assertEqual(response.context['search_query'], 'ویدیو')
    
    def test_product_filter(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {'product': 'laptop'})
        self.assertEqual(len(response.context['videos']), 2)  # video1 and video3 are for laptop
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video3, response.context['videos'])
        self.assertEqual(response.context['selected_product'], 'laptop')
    
    def test_language_filter_fa(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {'language': 'fa'})
        self.assertEqual(len(response.context['videos']), 2)  # video1 and video2 have Persian titles
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video2, response.context['videos'])
        self.assertEqual(response.context['selected_language'], 'fa')
    
    def test_language_filter_en(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {'language': 'en'})
        self.assertEqual(len(response.context['videos']), 2)  # video1 and video3 have English titles
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video3, response.context['videos'])
        self.assertEqual(response.context['selected_language'], 'en')
    
    # def test_date_range_filter(self):
    #     self.client.force_login(self.admin_user)
    #     today = timezone.now().date()
    #     yesterday = today - datetime.timedelta(days=1)
        
    #     # Filter for videos created in the last 2 days
    #     response = self.client.get(self.url, {
    #         'start_date': yesterday.strftime('%Y-%m-%d'),
    #         'end_date': today.strftime('%Y-%m-%d')
    #     })
        
    #     self.assertEqual(len(response.context['videos']), 2)  # video2 and video3
    #     self.assertIn(self.video2, response.context['videos'])
    #     self.assertIn(self.video3, response.context['videos'])
    #     self.assertEqual(response.context['start_date'], yesterday.strftime('%Y-%m-%d'))
    #     self.assertEqual(response.context['end_date'], today.strftime('%Y-%m-%d'))
    
    def test_has_cover_filter(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url, {'has_cover': 'on'})
        self.assertEqual(len(response.context['videos']), 2)  # video1 and video3 have covers
        self.assertIn(self.video1, response.context['videos'])
        self.assertIn(self.video3, response.context['videos'])
        self.assertTrue(response.context['has_cover'])
    
    def test_products_in_context(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])
        self.assertEqual(len(response.context['products']), 2)
    
    def test_ordering(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        videos = list(response.context['videos'])
        
        # Should be ordered by -created_date (newest first)
        self.assertEqual(videos[0], self.video3)
        self.assertEqual(videos[1], self.video2)
        self.assertEqual(videos[2], self.video1)