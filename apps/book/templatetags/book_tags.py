from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def book_icon(book, size="md"):
    context = {'book': book}
    
    if size == "sm":
        return mark_safe(render_to_string('components/_book_image_sm.html', context))
    elif size == "md":
        return mark_safe(render_to_string('components/_book_image_md.html', context))
    else:
        return mark_safe("<!-- Invalid image size specified -->")

@register.simple_tag
def bookshelf(books):
    """本棚を表示する"""
    context = {'books': books}
    return mark_safe(render_to_string('components/_bookshelf.html', context))

@register.simple_tag
def booklist(books):
    """本のリストを表示する"""
    context = {'books': books}
    return mark_safe(render_to_string('components/_booklist.html', context))