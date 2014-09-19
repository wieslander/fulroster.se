from django import template

register = template.Library()

@register.filter
def round(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return str(value)
    elif value < 10000:
        thousands = value / 1000.0
        return '%.1fk' % thousands
    else:
        thousands = value / 1000
        return '%dk' % thousands
