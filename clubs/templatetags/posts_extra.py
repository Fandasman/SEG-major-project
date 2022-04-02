# blog/templatetags/blog_extras.py
from django import template

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__

@register.filter
def has_liked_filter(value,user):
    return value.has_liked(user)
