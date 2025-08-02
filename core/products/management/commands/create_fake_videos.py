from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
import random
from django.core.files import File
from django.contrib.auth import get_user_model
from ...models import Product, ProductVideos  # Update with your actual model imports
import os
from django.conf import settings
from django.utils.text import slugify

User = get_user_model()

class PersianProvider(BaseProvider):
    def persian_word(self):
        persian_words = [
            "گجت", "ابزار", "وسیله", "دستگاه", "محصول",
            "کالا", "آیتم", "شیء", "ماده", "چیز",
            "مصنوعات", "ساخته", "تولید", "صنعتی", "مصرفی"
        ]
        return self.random_element(persian_words)
    
    def persian_sentence(self):
        words = [
            "این", "یک", "محصول", "است", "که", "می‌تواند", "مورد", "استفاده", "قرار", "گیرد",
            "برای", "مصارف", "مختلف", "در", "زندگی", "روزمره", "کاربرد", "دارد", "و", "می‌توان",
            "از", "آن", "به", "عنوان", "وسیله‌ای", "کارآمد", "استفاده", "کرد", "این", "محصول",
            "دارای", "ویژگی‌های", "مختلفی", "است", "که", "آن", "را", "از", "سایر", "محصولات",
            "متمایز", "می‌کند", "کیفیت", "بالا", "و", "قیمت", "مناسب", "از", "مزایای", "این",
            "محصول", "به", "شمار", "می‌رود"
        ]
        sentence = ' '.join([self.random_element(words) for _ in range(random.randint(5, 15))])
        return sentence + "."

class Command(BaseCommand):
    help = 'Generates fake product videos with covers from local folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake videos to create (default: 10)'
        )
        parser.add_argument(
            '--image-folder',
            type=str,
            default='image_folder_for_fake_product',
            help='Path to folder containing sample cover images (relative to MEDIA_ROOT)'
        )
        parser.add_argument(
            '--product-count',
            type=int,
            default=3,
            help='Number of products to associate with each video (default: 3)'
        )

    def handle(self, *args, **options):
        fake = Faker('fa_IR')  # Use Persian locale
        fake.add_provider(PersianProvider)
        Faker.seed(0)  # For consistent results

        count = options['count']
        image_folder = options['image_folder']
        product_count = options['product_count']
        created_count = 0

        # Get or create a test user
        try:
            user = User.objects.get_or_create(
                email='video_creator@example.com',
                defaults={
                    'password': 'testpass123'
                }
            )[0]
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting test user: {e}'))
            return

        # Get some products
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please create some products first.'))
            return

        # Get list of available cover images
        image_dir = os.path.join(settings.MEDIA_ROOT, image_folder)
        if not os.path.exists(image_dir):
            self.stdout.write(self.style.ERROR(f'Image folder not found: {image_dir}'))
            return

        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            self.stdout.write(self.style.ERROR(f'No images found in folder: {image_dir}'))
            return

        # Common video platforms for URL examples
        video_platforms = [
            # 'youtube.com/watch?v=',
            # 'vimeo.com/',
            'dailymotion.com/video/',
            'aparat.com/v/'
        ]

        for i in range(count):
            # Generate random video title
            title_en = f"Product Video {fake.random_int(1000, 9999)}"
            title_fa = f"ویدیوی معرفی {fake.persian_word()} {fake.random_int(100, 999)}"
            
            # Generate video data
            video_data = {
                'user': user,
                'title_en': title_en,
                'title_fa': title_fa,
                'description': fake.persian_sentence() * 3,
                'video_url': f"https://{random.choice(video_platforms)}{fake.unique.uuid4()}"
            }

            try:
                # Create the video first to generate slug for cover path
                video = ProductVideos(**video_data)
                video.save()  # This will generate the slug

                # Select a random cover image from the folder
                random_image = random.choice(image_files)
                image_path = os.path.join(image_dir, random_image)

                # Save the cover image to the video
                with open(image_path, 'rb') as f:
                    filename = f"video_cover_{video.slug}{os.path.splitext(random_image)[1]}"
                    video.cover.save(filename, File(f))
                    video.save()

                # Add random products (1 to product_count products per video)
                num_products = random.randint(1, min(product_count, len(products)))
                video.product.add(*random.sample(list(products), num_products))

                created_count += 1
                self.stdout.write(f"Created video: {video.title_en}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating video: {e}'))
                if 'video' in locals() and video.pk:
                    video.delete()  # Clean up if video was created but cover failed

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} product videos with covers from {image_dir}.')
        )