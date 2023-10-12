from django import template

register = template.Library()

@register.filter
def is_following(user, target_user):
    return user.is_following(target_user)
