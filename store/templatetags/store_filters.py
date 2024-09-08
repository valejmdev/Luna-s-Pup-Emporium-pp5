from django import template

register = template.Library()


@register.filter
def range_filter(value):
    """Returns a list of numbers from 1 to the given value."""
    try:
        value = int(value)
        return range(1, value + 1)
    except ValueError:
        return []
