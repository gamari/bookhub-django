from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def book_icon(book, size="md"):
    print(book)
    context = {'book': book}
    
    if size == "sm":
        return mark_safe(render_to_string('components/_book_image_sm.html', context))
    elif size == "md":
        return mark_safe(render_to_string('components/_book_image_md.html', context))
    else:
        return mark_safe("<!-- Invalid image size specified -->")
