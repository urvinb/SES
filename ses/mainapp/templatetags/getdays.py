from django import template
register = template.Library()

@register.filter
def get_days(obj):
    return obj.get_left_days()