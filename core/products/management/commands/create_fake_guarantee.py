from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from ...models import ProductGuarantee  # Update with your actual model import path

class Command(BaseCommand):
    help = 'Generates fake product guarantees'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake guarantees to create (default: 10)'
        )

    def handle(self, *args, **options):
        fake = Faker(['en_US', 'fa_IR'])  # Use both English and Persian locales
        count = options['count']
        created_count = 0

        # Common guarantee types in English and Persian with descriptions
        guarantee_types = [
            {
                "en": "1 Year Warranty",
                "fa": "گارانتی 1 ساله",
                "desc": "One year manufacturer warranty covering defects in materials and workmanship"
            },
            {
                "en": "2 Year Warranty",
                "fa": "گارانتی 2 ساله",
                "desc": "Two years comprehensive warranty with free repair service"
            },
            {
                "en": "6 Month Warranty",
                "fa": "گارانتی 6 ماهه",
                "desc": "Six months limited warranty covering major defects"
            },
            {
                "en": "Lifetime Warranty",
                "fa": "گارانتی مادام العمر",
                "desc": "Lifetime coverage for manufacturing defects"
            },
            {
                "en": "3 Year Extended Warranty",
                "fa": "گارانتی 3 ساله گسترده",
                "desc": "Three years extended warranty with optional service plans"
            },
            {
                "en": "90 Day Warranty",
                "fa": "گارانتی 90 روزه",
                "desc": "90 days money back guarantee"
            },
            {
                "en": "5 Year Limited Warranty",
                "fa": "گارانتی 5 ساله محدود",
                "desc": "Five years limited warranty covering specific components"
            },
            {
                "en": "International Warranty",
                "fa": "گارانتی بین المللی",
                "desc": "Global warranty coverage in authorized service centers worldwide"
            },
            {
                "en": "No Warranty",
                "fa": "بدون گارانتی",
                "desc": "Sold as-is with no warranty coverage"
            },
            {
                "en": "30 Day Return Policy",
                "fa": "سیاست بازگشت 30 روزه",
                "desc": "30 days return policy with full refund"
            },
        ]

        for i in range(count):
            # Use predefined guarantees first, then generate random ones
            if i < len(guarantee_types):
                guarantee_data = guarantee_types[i]
                title_en = guarantee_data["en"]
                title_fa = guarantee_data["fa"]
                description = guarantee_data["desc"]
            else:
                # Generate random guarantee names if we've exhausted the common ones
                periods = ["Month", "Year"]
                numbers = ["6", "12", "18", "24", "36", "60"]
                types = ["Limited", "Full", "Extended", "International", "Premium"]
                
                period = fake.random_element(periods)
                number = fake.random_element(numbers)
                type = fake.random_element(types)
                
                title_en = f"{number} {period} {type} Warranty"
                title_fa = f"گارانتی {type} {number} {period}ه"
                description = f"This {type.lower()} warranty covers the product for {number} {period.lower()}s"

            try:
                guarantee = ProductGuarantee(
                    title_en=title_en,
                    title_fa=title_fa,
                    description=description,
                )
                guarantee.save()  # This will generate the slug automatically
                created_count += 1
                self.stdout.write(f"Created guarantee: {title_en} / {title_fa}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating guarantee: {e}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} product guarantees.')
        )