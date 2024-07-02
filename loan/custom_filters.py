from django import template
register = template.Library()

@register.filter
def subtract(value, arg):
    val = str(value - arg).strip(",")[0]
    return val
