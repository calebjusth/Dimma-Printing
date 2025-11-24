from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return round(value / int(arg))
    except (ValueError, ZeroDivisionError, TypeError):
        return None
