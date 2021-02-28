from django import template
register = template.Library()

@register.filter
def get_subscribed(obj,user):
    return obj.get_is_subscribed(user)

