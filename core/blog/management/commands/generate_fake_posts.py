from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from django.contrib.auth import get_user_model
import os
from django.conf import settings
import random
from django.core.files import File


from ...models import Post, Category, Tag  # Replace 'your_app' with your actual app name

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake data for Post model'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Check if we have users, categories, and tags
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return
            
        categories = Category.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create categories first.'))
            return
            
        tags = Tag.objects.all()
        if not tags.exists():
            self.stdout.write(self.style.ERROR('No tags found. Please create tags first.'))
            return
        
        # Predefined Persian and English content
        persian_content_samples = [
            "در دنیای امروز، فناوری اطلاعات نقش بسیار مهمی در زندگی روزمره ما ایفا می‌کند. این مقاله به بررسی تاثیرات مختلف فناوری بر جامعه می‌پردازد.",
            "یادگیری ماشین و هوش مصنوعی در حال تغییر جهان هستند. در این مطلب، به بررسی کاربردهای مختلف این تکنولوژی‌ها می‌پردازیم.",
            "برنامه‌نویسی یکی از مهارت‌های اساسی در دنیای دیجیتال است. این مقاله به معرفی زبان‌های برنامه‌نویسی محبوب می‌پردازد.",
            "امنیت سایبری موضوع بسیار مهمی در عصر دیجیتال است. در این مطلب، راهکارهای مختلف برای محافظت از داده‌ها ارائه می‌شود.",
            "توسعه وب یکی از حوزه‌های پرطرفدار در فناوری اطلاعات است. این مقاله به معرفی فریم‌ورک‌های مدرن وب می‌پردازد.",
            "داده‌کاوی و تحلیل داده‌ها به کسب‌وکارها کمک می‌کند تا تصمیمات بهتری بگیرند. در این مطلب، روش‌های مختلف تحلیل داده بررسی می‌شود.",
            "شبکه‌های اجتماعی تاثیر عمیقی بر ارتباطات انسانی دارند. این مقاله به بررسی اثرات مثبت و منفی این پلتفرم‌ها می‌پردازد.",
            "اپلیکیشن‌های موبایل زندگی ما را متحول کرده‌اند. در این مطلب، به بررسی روند توسعه اپلیکیشن‌های موبایل می‌پردازیم.",
            "بازاریابی دیجیتال یکی از ارکان اصلی کسب‌وکارهای امروزی است. این مقاله به معرفی استراتژی‌های موثر بازاریابی می‌پردازد.",
            "طراحی用户体验 (UX) نقش کلیدی در موفقیت محصولات دیجیتال دارد. در این مطلب، اصول طراحی کاربرپسند بررسی می‌شود."
        ]
        
        english_content_samples = [
            "In today's world, information technology plays a crucial role in our daily lives. This article explores the various impacts of technology on society.",
            "Machine learning and artificial intelligence are changing the world. In this post, we examine the different applications of these technologies.",
            "Programming is one of the essential skills in the digital world. This article introduces popular programming languages and their uses.",
            "Cybersecurity is a critical topic in the digital age. This post provides various solutions for protecting data and privacy.",
            "Web development is one of the most popular fields in IT. This article introduces modern web frameworks and their capabilities.",
            "Data mining and analysis help businesses make better decisions. This post examines different data analysis methods and techniques.",
            "Social media has a profound impact on human communication. This article explores both positive and negative effects of these platforms.",
            "Mobile applications have transformed our lives. In this post, we discuss mobile app development trends and best practices.",
            "Digital marketing is a cornerstone of modern businesses. This article introduces effective marketing strategies and approaches.",
            "User Experience (UX) design plays a key role in digital product success. This post examines principles of user-centered design."
        ]
        
        persian_titles = [
            "تاثیر فناوری بر جامعه مدرن",
            "هوش مصنوعی و آینده بشر",
            "آموزش برنامه‌نویسی برای مبتدیان",
            "امنیت اطلاعات در دنیای دیجیتال",
            "توسعه وب با فریم‌ورک‌های مدرن",
            "تحلیل داده‌ها برای کسب‌وکار",
            "شبکه‌های اجتماعی و ارتباطات",
            "توسعه اپلیکیشن‌های موبایل",
            "استراتژی‌های بازاریابی دیجیتال",
            "اصول طراحی用户体验"
        ]
        
        english_titles = [
            "The Impact of Technology on Modern Society",
            "Artificial Intelligence and the Future of Humanity",
            "Programming Education for Beginners",
            "Information Security in the Digital World",
            "Web Development with Modern Frameworks",
            "Data Analysis for Business Growth",
            "Social Media and Human Connections",
            "Mobile Application Development Trends",
            "Digital Marketing Strategies for Success",
            "Principles of User Experience Design"
        ]
        
        # Check for existing images
        image_dir = os.path.join(settings.MEDIA_ROOT, "image_folder_for_fake_post")
        if not os.path.exists(image_dir):
            os.makedirs(image_dir, exist_ok=True)
        
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            self.stdout.write(self.style.WARNING(f'No images found in folder: {image_dir}'))
            self.stdout.write(self.style.WARNING('Posts will be created without images or with placeholder names'))
            # Create some placeholder image names
            image_files = [f"post-image-{i}.jpg" for i in range(1, 11)]
        
        # Generate 10 fake Posts
        self.stdout.write("Generating fake Posts...")
        for i in range(10):
            try:
                # Select random user, categories, and tags
                user = fake.random_element(elements=users)
                selected_categories = fake.random_elements(elements=list(categories), length=random.randint(1, 3), unique=True)
                selected_tags = fake.random_elements(elements=list(tags), length=random.randint(2, 5), unique=True)
                
                persian_content_elemets = fake.random_elements(elements=persian_content_samples, length=random.randint(3,5), unique=True)
                title_en_elements = fake.random_elements(elements=english_titles, length=random.randint(3,5), unique=True)
                persian_content = " ".join(persian_content_elemets)
                title_en = " ".join(title_en_elements)

                
                # Select status with weighted probability (more published posts)
                status_options = [Post.DRAFT, Post.PUBLISHED, Post.ARCHIVED]
                status_weights = [0.2, 0.7, 0.1]  # draft, published, archived
                status = random.choices(status_options, weights=status_weights, k=1)[0]
                
                # Set dates appropriately
                created_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                
                if status == Post.PUBLISHED:
                    published_date = fake.date_time_between(start_date=created_date, end_date='now', tzinfo=timezone.get_current_timezone())
                else:
                    published_date = None
                
                post = Post(
                    title_en=title_en,
                    title_fa=persian_titles[i],
                    content=persian_content,
                    excerpt=fake.sentence(nb_words=15),
                    image=f"blog_images/{fake.random_element(elements=image_files)}",
                    status=status,
                    user=user,
                    created_date=created_date,
                    updated_date=fake.date_time_between(start_date=created_date, end_date='now', tzinfo=timezone.get_current_timezone()),
                    published_date=published_date,
                    views=fake.random_int(min=0, max=1000),
                    featured=fake.boolean(chance_of_getting_true=30),
                    meta_description=fake.sentence(nb_words=10)
                )
                
                # Save the post first to get an ID
                post.save()
                
                # Select a random image from the folder
                random_image = random.choice(image_files)
                image_path = os.path.join(image_dir, random_image)

                # Save the image to the product
                with open(image_path, 'rb') as f:
                    filename = f"product_{post.slug}{os.path.splitext(random_image)[1]}"
                    post.image.save(filename, File(f))
                    post.save()
                    
                # Add many-to-many relationships
                post.categories.set(selected_categories)
                post.tags.set(selected_tags)
                
                self.stdout.write(self.style.SUCCESS(f'Created Post: {post.title_en} (Status: {post.status})'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating Post {i+1}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 Posts with Persian and English content!'))