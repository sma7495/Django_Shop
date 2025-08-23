from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
import jdatetime
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def persian_intcomma(value):
    persian_digits = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    formatted = intcomma(value)
    for eng, per in persian_digits.items():
        formatted = formatted.replace(eng, per)
    return formatted


@register.simple_tag(name = "utc_to_jalali")
def fun(date):
    jdatetime.set_locale(jdatetime.FA_LOCALE)
    return jdatetime.datetime.fromgregorian(datetime=date).strftime("%d-%B-%Y")



@register.simple_tag(name="jalali_to_utc")
def jalali_to_utc(jalali_date_string, date_format="%d-%B-%Y"):
    """
    Convert Jalali (FA_LOCALE) date string to UTC datetime
    Usage: {% jalali_to_utc your_jalali_date_string %}
    """
    try:
        # Set Farsi locale for parsing
        jdatetime.set_locale(jdatetime.FA_LOCALE)
        
        # Parse the Jalali date string
        jalali_date = jdatetime.datetime.strptime(jalali_date_string, date_format)
        
        # Convert to Gregorian datetime
        gregorian_date = jalali_date.togregorian()
        
        # Make it timezone aware (UTC)
        utc_date = timezone.make_aware(gregorian_date, timezone.utc)
        
        return utc_date
        
    except ValueError:
        # Handle invalid date format
        return None


    
