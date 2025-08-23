from django import template
from django.contrib.auth import get_user_model
from ..models import Profile  # Import your profile model


User = get_user_model()

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_profile(context):
    """
    Returns the user profile for the currently logged-in user.
    Usage: {% get_user_profile as profile %}
    """
    request = context.get('request')
    if request and request.user.is_authenticated:
        try:
            # Adjust this based on your profile model structure
            return Profile.objects.get(id=request.user.id)
        except Profile.DoesNotExist:
            return None
    return None
