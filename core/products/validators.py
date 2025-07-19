# myapp/validators.py
import re
from django.core.exceptions import ValidationError

def validate_english(value):
    """Checks if text contains only English characters"""
    if not re.match(r'^[a-zA-Z0-9\s\-.,!?@\'"()]+$', value):
        raise ValidationError(
            'English title must contain only English letters, numbers, and basic punctuation.',
            code='invalid_english'
        )

def validate_persian(value):
    """Checks if text contains Persian characters (and allows spaces/punctuation)"""
    persian_regex = r'^[\u0600-\u06FF\s\-.,!?@\'"()۰-۹]+$'
    if not re.match(persian_regex, value):
        raise ValidationError(
            'Persian title must contain Persian characters (فارسی) and Arabic-script punctuation.',
            code='invalid_persian'
        )