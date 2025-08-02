from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from ...models import ProductColor  # Update with your actual model import path

class Command(BaseCommand):
    help = 'Generates fake product colors'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake colors to create (default: 10)'
        )

    def handle(self, *args, **options):
        fake = Faker(['en_US', 'fa_IR'])  # Use both English and Persian locales
        count = options['count']
        created_count = 0

        # Common color names in English and Persian
        color_pairs = [
            {"en": "Red", "fa": "قرمز"},
            {"en": "Blue", "fa": "آبی"},
            {"en": "Green", "fa": "سبز"},
            {"en": "Yellow", "fa": "زرد"},
            {"en": "Black", "fa": "مشکی"},
            {"en": "White", "fa": "سفید"},
            {"en": "Silver", "fa": "نقره‌ای"},
            {"en": "Gold", "fa": "طلایی"},
            {"en": "Purple", "fa": "بنفش"},
            {"en": "Orange", "fa": "نارنجی"},
            {"en": "Pink", "fa": "صورتی"},
            {"en": "Brown", "fa": "قهوه‌ای"},
            {"en": "Gray", "fa": "خاکستری"},
            {"en": "Turquoise", "fa": "فیروزه‌ای"},
            {"en": "Navy Blue", "fa": "آبی نفتی"},
            {"en": "Beige", "fa": "بژ"},
            {"en": "Maroon", "fa": "خرمایی"},
            {"en": "Olive", "fa": "زیتونی"},
            {"en": "Teal", "fa": "سبز آبی"},
            {"en": "Lavender", "fa": "اسطوخودوسی"},
        ]

        for i in range(count):
            # Use predefined colors first, then generate random ones
            if i < len(color_pairs):
                color_data = color_pairs[i]
                title_en = color_data["en"]
                title_fa = color_data["fa"]
            else:
                # Generate random color names if we've exhausted the common ones
                title_en = fake.color_name()
                title_fa = f"{fake.word(ext_word_list=['رنگ', 'گونه'])} {fake.word(ext_word_list=['طبیعی', 'جذاب', 'شیک', 'مدرن'])}"

            try:
                color = ProductColor(
                    title_en=title_en,
                    title_fa=title_fa,
                )
                color.save()  # This will generate the slug automatically
                created_count += 1
                self.stdout.write(f"Created color: {title_en} / {title_fa}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating color: {e}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} product colors.')
        )