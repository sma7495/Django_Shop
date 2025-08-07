from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

@register.filter
def persian_intcomma(value):
    persian_digits = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    formatted = intcomma(value)
    for eng, per in persian_digits.items():
        formatted = formatted.replace(eng, per)
    return formatted