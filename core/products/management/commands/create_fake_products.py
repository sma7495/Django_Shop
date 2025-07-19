from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
import random
from decimal import Decimal
from django.core.files import File
from django.contrib.auth import get_user_model
from ...models import Product, ProductCategory  # Replace 'your_app' with your app name
import os
from django.conf import settings

User = get_user_model()

class PersianProvider(BaseProvider):
    def persian_word(self):
        persian_words = [
            "الکترونیک", "لباس", "کتاب", "خانه", "باغ", 
            "ورزشی", "زیبایی", "اسباب‌بازی", "غذا", "مبلمان",
            "جواهرات", "کامپیوتر", "موبایل", "تلویزیون", "یخچال"
        ]
        return self.random_element(persian_words)

class Command(BaseCommand):
    help = 'Generates fake products with images from local folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake products to create (default: 10)'
        )
        parser.add_argument(
            '--image-folder',
            type=str,
            default='image_folder_for_fake_product',
            help='Path to folder containing sample images (relative to MEDIA_ROOT)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(PersianProvider)
        Faker.seed(0)  # For consistent results

        count = options['count']
        image_folder = options['image_folder']
        created_count = 0

        # Get or create a test user
        try:
            user = User.objects.get_or_create(
                email='seller@example.com',
                defaults={
                    'password': 'testpass123'
                }
            )[0]
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting test user: {e}'))
            return

        # Get some categories
        categories = ProductCategory.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create some categories first.'))
            return

        # Get list of available images
        image_dir = os.path.join(settings.MEDIA_ROOT, image_folder)
        if not os.path.exists(image_dir):
            self.stdout.write(self.style.ERROR(f'Image folder not found: {image_dir}'))
            return

        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            self.stdout.write(self.style.ERROR(f'No images found in folder: {image_dir}'))
            return

        # English-Persian product name pairs
        product_pairs = [
            ("Smartphone", "تلفن همراه هوشمند"),
            ("Laptop", "لپ تاپ"),
            ("T-Shirt", "تی شرت"),
            ("Book", "کتاب"),
            ("Watch", "ساعت"),
            ("Headphones", "هدفون"),
            ("Shoes", "کفش"),
            ("Backpack", "کوله پشتی"),
            ("Camera", "دوربین"),
            ("Tablet", "تبلت")
        ]

        for i in range(count):
            # Get or create a pair (cycling through the list if count > 10)
            title_en, title_fa = product_pairs[i % len(product_pairs)]

            # Generate random product data
            product_data = {
                'user': user,
                'title_en': f"{title_en} {fake.word().capitalize()}",
                'title_fa': f"{title_fa} {fake.persian_word()}",
                'description': fake.paragraph(nb_sentences=5),
                'brief_description': fake.sentence(nb_words=10),
                'stock': random.randint(0, 100),
                'price': Decimal(random.randint(10000, 1000000)),  # Assuming IRR currency
                'discount_percent': random.choice([0, 0, 0, 5, 10, 15]),  # Mostly no discount
                'status': random.choice(['draft', 'published'])
            }

            try:
                # Create the product first to generate slug for image path
                product = Product(**product_data)
                product.save()  # This will generate the slug

                # Select a random image from the folder
                random_image = random.choice(image_files)
                image_path = os.path.join(image_dir, random_image)

                # Save the image to the product
                with open(image_path, 'rb') as f:
                    filename = f"product_{product.slug}{os.path.splitext(random_image)[1]}"
                    product.image.save(filename, File(f))
                    product.save()

                # Add random categories (1-3 categories per product)
                num_categories = random.randint(1, 3)
                product.category.add(*random.sample(list(categories), num_categories))

                created_count += 1
                self.stdout.write(f"Created product: {product.title_en} with image {random_image}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating product: {e}'))
                if 'product' in locals() and product.pk:
                    product.delete()  # Clean up if product was created but image failed

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count}/{count} fake products with images from {image_dir}.')
        )