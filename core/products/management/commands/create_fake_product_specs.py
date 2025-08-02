from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
import random
from django.contrib.auth import get_user_model
from ...models import Product, ProductSpecifications  # Update with your actual model imports
from django.utils.text import slugify

User = get_user_model()

class PersianProvider(BaseProvider):
    def persian_word(self):
        persian_words = [
            "ویژگی", "مشخصه", "خصوصیت", "قابلیت", "کارایی",
            "عملکرد", "جزئیات", "اطلاعات", "توضیحات", "مشخصات",
            "تکنیکال", "فنی", "سخت‌افزاری", "نرم‌افزاری", "ابعاد"
        ]
        return self.random_element(persian_words)
    
    def persian_sentence(self):
        words = [
            "این", "مشخصه", "نشان‌دهنده", "است", "که", "محصول", "دارای",
            "ویژگی", "خاصی", "می‌باشد", "و", "می‌تواند", "برای", "استفاده",
            "در", "شرایط", "مختلف", "مناسب", "باشد", "این", "قابلیت",
            "به", "شما", "کمک", "می‌کند", "تا", "بهترین", "استفاده", "را",
            "از", "محصول", "ببرید", "و", "رضایت", "کامل", "داشته", "باشید"
        ]
        sentence = ' '.join([self.random_element(words) for _ in range(random.randint(5, 10))])
        return sentence + "."
    
    def specification_value(self):
        values = [
            "بله", "خیر", "دارد", "ندارد", "24 ماه", "12 ماه", 
            "1 سال", "2 سال", "مادام‌العمر", "100 گرم", "500 گرم",
            "1 کیلوگرم", "2 کیلوگرم", "30 سانتی‌متر", "50 سانتی‌متر",
            "1 متر", "1.5 متر", "پلاستیک", "فلز", "چوب", "شیشه",
            "نسوز", "ضد آب", "ضد ضربه", "USB-C", "بلوتوث", "وای‌فای",
            "5.0", "4.2", "1080p", "4K", "8GB", "16GB", "32GB"
        ]
        return self.random_element(values)

class Command(BaseCommand):
    help = 'Generates fake product specifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake specifications to create (default: 10)'
        )
        parser.add_argument(
            '--specs-per-product',
            type=int,
            default=3,
            help='Number of specifications to create per product (default: 3)'
        )

    def handle(self, *args, **options):
        fake = Faker('fa_IR')  # Use Persian locale
        fake.add_provider(PersianProvider)
        Faker.seed(0)  # For consistent results

        count = options['count']
        specs_per_product = options['specs_per_product']
        created_count = 0

        # Get some products
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please create some products first.'))
            return

        # Common specification titles in English and Persian
        spec_titles = [
            {"en": "Warranty", "fa": "گارانتی"},
            {"en": "Weight", "fa": "وزن"},
            {"en": "Dimensions", "fa": "ابعاد"},
            {"en": "Color", "fa": "رنگ"},
            {"en": "Material", "fa": "جنس"},
            {"en": "Connectivity", "fa": "اتصال"},
            {"en": "Battery Life", "fa": "طول عمر باتری"},
            {"en": "Resolution", "fa": "رزولوشن"},
            {"en": "Storage", "fa": "حافظه"},
            {"en": "Waterproof", "fa": "ضد آب"},
            {"en": "Bluetooth Version", "fa": "نسخه بلوتوث"},
            {"en": "Warranty Period", "fa": "دوره گارانتی"},
        ]

        for product in products:
            # Create multiple specifications for each product
            for i in range(min(specs_per_product, len(spec_titles))):
                # Either use a common spec or make a random one
                if random.choice([True, False]) and spec_titles:
                    spec_title = spec_titles.pop()
                    title_en = spec_title["en"]
                    title_fa = spec_title["fa"]
                else:
                    title_en = f"Spec {fake.random_int(1, 100)}"
                    title_fa = f"{fake.persian_word()} {fake.random_int(1, 100)}"

                spec_data = {
                    'product': product,
                    'title_en': title_en,
                    'title_fa': title_fa,
                    'value': fake.specification_value(),
                }

                try:
                    ProductSpecifications.objects.create(**spec_data)
                    created_count += 1
                    self.stdout.write(f"Created specification '{title_en}' for product {product.title_en}")
                    
                    # Stop if we've reached the total count
                    if created_count >= count:
                        break
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating specification: {e}'))

            if created_count >= count:
                break

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} product specifications.')
        )