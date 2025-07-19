from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
from ...models import ProductCategory  # Replace 'your_app' with your actual app name


class PersianProvider(BaseProvider):
    def persian_word(self):
        persian_words = [
            "الکترونیک", "لباس", "کتاب", "خانه", "باغ", 
            "ورزشی", "زیبایی", "اسباب‌بازی", "غذا", "مبلمان",
            "جواهرات", "کامپیوتر", "موبایل", "تلویزیون", "یخچال"
        ]
        return self.random_element(persian_words)


class Command(BaseCommand):
    help = 'Generates fake product categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake categories to create (default: 10)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(PersianProvider)
        Faker.seed(0)  # For consistent results

        count = options['count']

        # Create English-Persian word pairs for more realistic data
        category_pairs = [
            ("Electronics", "الکترونیک"),
            ("Clothing", "لباس"),
            ("Books", "کتاب‌ها"),
            ("Home & Garden", "خانه و باغ"),
            ("Sports", "ورزشی"),
            ("Beauty", "زیبایی"),
            ("Toys", "اسباب‌بازی"),
            ("Food", "غذا"),
            ("Furniture", "مبلمان"),
            ("Jewelry", "جواهرات")
        ]

        created_count = 0

        for i in range(count):
            # Get or create a pair (cycling through the list if count > 10)
            title_en, title_fa = category_pairs[i % len(category_pairs)]

            try:
                ProductCategory.objects.create(
                    title_en=title_en,
                    title_fa=title_fa,
                    # Slug will be auto-generated in the save() method
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating category: {e}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count}/{count} fake categories.')
        )