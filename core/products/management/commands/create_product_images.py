from django.core.management.base import BaseCommand
from ...models import Product, ProductImage  # Replace 'your_app' with your app name
import os
import random
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Generates product images for existing products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--image-folder',
            type=str,
            default='image_folder_for_fake_product',
            help='Path to folder containing sample images (relative to MEDIA_ROOT)'
        )
        parser.add_argument(
            '--min-images',
            type=int,
            default=3,
            help='Minimum number of images per product (default: 3)'
        )
        parser.add_argument(
            '--max-images',
            type=int,
            default=5,
            help='Maximum number of images per product (default: 5)'
        )

    def handle(self, *args, **options):
        image_folder = options['image_folder']
        min_images = options['min_images']
        max_images = options['max_images']
        
        # Get list of available images
        image_dir = os.path.join(settings.MEDIA_ROOT, image_folder)
        if not os.path.exists(image_dir):
            self.stdout.write(self.style.ERROR(f'Image folder not found: {image_dir}'))
            return

        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            self.stdout.write(self.style.ERROR(f'No images found in folder: {image_dir}'))
            return

        # Get all products that need images
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please create some products first.'))
            return

        total_created = 0

        for product in products:
            # Determine how many images to add for this product
            num_images = random.randint(min_images, max_images)
            created_for_product = 0

            for i in range(num_images):
                try:
                    # Select a random image from the folder
                    random_image = random.choice(image_files)
                    image_path = os.path.join(image_dir, random_image)

                    # Create the ProductImage instance
                    with open(image_path, 'rb') as f:
                        # Generate unique filename using product slug and index
                        filename = f"product_{product.slug}_{i}{os.path.splitext(random_image)[1]}"
                        
                        product_image = ProductImage(
                            product=product,
                        )
                        product_image.image.save(filename, File(f))
                        product_image.save()

                    created_for_product += 1
                    total_created += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating image for product {product.id}: {e}'))

            if created_for_product > 0:
                self.stdout.write(f"Added {created_for_product} images to product: {product.title_en}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {total_created} product images from {image_dir}.')
        )