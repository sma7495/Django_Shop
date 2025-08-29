# your_app/templatetags/product_tags.py

from django import template
from django.db.models import Count, Q
from django.db.models.functions import Coalesce

from ..models import Category, Post

register = template.Library()

# @register.simple_tag(name = "get_post_data_base_category")
# def fun():
#     category = Category.objects.all()
#     published_posts = []
#     not_published_posts = []
#     for cat in category:
#         not_published_posts.append(Post.objects.filter(category = cat, status = Post.DRAFT).count())
#         published_posts.append(Post.objects.filter(category = cat, status__in = [Post.PUBLISHED, Post.ARCHIVED]).count())
#     return {
#         'all' : Post.objects.all().count(),
#         'category' : category,
#         'published_posts':published_posts,
#         'not_published_posts' :not_published_posts,
#     }
@register.simple_tag(name="get_post_data_base_category")
def get_post_statistics():
    """
    Returns post statistics by category, optimized for database performance.
    """
    # Get all categories with annotated counts
    categories = Category.objects.annotate(
        published_count=Coalesce(
            Count('post', filter=Q(post__status__in=[Post.PUBLISHED, Post.ARCHIVED])),
            0
        ),
        draft_count=Coalesce(
            Count('post', filter=Q(post__status=Post.DRAFT)),
            0
        )
    )
    
    # Extract the counts into separate lists
    published_posts = [cat.published_count for cat in categories]
    not_published_posts = [cat.draft_count for cat in categories]
    
    # Get total post count (more efficient than counting all objects)
    total_posts = Post.objects.all().count()
    
    # Convert categories to a list of dictionaries for serialization
    category_list = [cat.title_fa for cat in categories]
    return {
        'all': total_posts,
        'category': category_list,
        'published_posts': published_posts,
        'not_published_posts': not_published_posts,
    }
    