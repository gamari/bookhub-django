from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from apps.book.models import Bookshelf

User = get_user_model()

register = template.Library()

# TODO search panel listで一括で取得できるようにする
@register.simple_tag
def search_panel(book, user: User=None):
    is_registered = False

    if user.is_authenticated:
        bookshelf: Bookshelf = user.bookshelf
        print(book)
        is_registered = bookshelf.contains(book)
        print(is_registered)

    context = {
        'book': book,
        'is_registered': is_registered
    }

    return mark_safe(render_to_string('components/_search_panel.html', context))
    