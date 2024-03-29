from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def review_list(reviews, is_authenticated=False):
    context = {
        "rating_range": range(1, 6), 
        "reviews": reviews,
        "is_authenticated": is_authenticated,
    }

    return mark_safe(render_to_string("components/_review_list.html", context))
