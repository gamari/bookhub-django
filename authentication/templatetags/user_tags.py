from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def user_icon(user, size="md"):
    context = {'user': user}
    print(size)
    
    if size == "xs":
        return mark_safe(render_to_string('components/_user_icon_xs.html', context))
    elif size == "sm":
        return mark_safe(render_to_string('components/_user_icon_sm.html', context))
    elif size == "md":
        return mark_safe(render_to_string('components/_user_icon_md.html', context))
    else:
        return mark_safe("<!-- Invalid icon size specified -->")
