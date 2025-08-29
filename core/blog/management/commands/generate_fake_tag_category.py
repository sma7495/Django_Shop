from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Category, Tag  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Generate fake data for Category and Tag models'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Predefined Persian categories with corresponding English translations
        persian_categories = [
            {"en": "Programming", "fa": "برنامه‌نویسی"},
            {"en": "Artificial Intelligence", "fa": "هوش مصنوعی"},
            {"en": "Web Development", "fa": "توسعه وب"},
            {"en": "Mobile Applications", "fa": "اپلیکیشن‌های موبایل"},
            {"en": "Data Science", "fa": "علم داده"},
            {"en": "Network Security", "fa": "امنیت شبکه"},
            {"en": "Graphic Design", "fa": "طراحی گرافیک"},
            {"en": "Digital Marketing", "fa": "بازاریابی دیجیتال"},
            {"en": "Health and Fitness", "fa": "سلامتی و تناسب اندام"},
            {"en": "Travel and Tourism", "fa": "سفر و گردشگری"}
        ]
        
        # Predefined Persian tags
        persian_tags = [
            {"en": "Python", "fa": "پایتون"},
            {"en": "JavaScript", "fa": "جاوااسکریپت"},
            {"en": "React", "fa": "ریکت"},
            {"en": "Django", "fa": "جنگو"},
            {"en": "Machine Learning", "fa": "یادگیری ماشین"},
            {"en": "Deep Learning", "fa": "یادگیری عمیق"},
            {"en": "CSS", "fa": "سی‌اس‌اس"},
            {"en": "HTML", "fa": "اچ‌تی‌ام‌ال"},
            {"en": "Database", "fa": "پایگاه داده"},
            {"en": "API", "fa": "ای‌پی‌آی"}
        ]
        
        # Predefined Persian descriptions
        persian_descriptions = [
            "مجموعه‌ای جامع از مطالب و مقالات مرتبط با {}",
            "منبعی غنی برای یادگیری و آموزش در زمینه {}",
            "جدیدترین اخبار و تحولات حوزه {}",
            "آموزش‌های تخصصی و کاربردی برای {}",
            "مرجع کاملی برای علاقه‌مندان به {}"
        ]

        # Generate 10 fake Categories
        self.stdout.write("Generating fake Categories...")
        for i in range(10):
            try:
                category_data = fake.random_element(elements=persian_categories)
                
                category = Category(
                    title_en=category_data["en"],
                    title_fa=category_data["fa"],
                    description=persian_descriptions[i % len(persian_descriptions)].format(category_data["fa"]),
                    is_active=fake.boolean(chance_of_getting_true=80)
                )
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Created Category: {category.title_en} -> {category.title_fa}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating Category: {e}'))
        
        # Generate 10 fake Tags
        self.stdout.write("Generating fake Tags...")
        for i in range(10):
            try:
                tag_data = persian_tags[i]  # Use each tag in sequence
                
                tag = Tag(
                    title_en=tag_data["en"],
                    title_fa=tag_data["fa"]
                )
                tag.save()
                self.stdout.write(self.style.SUCCESS(f'Created Tag: {tag.title_en} -> {tag.title_fa}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating Tag: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 Categories and 10 Tags with authentic Persian data!'))