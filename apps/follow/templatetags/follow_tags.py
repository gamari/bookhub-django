from django import template
from django.template.loader import render_to_string

from apps.follow.domain.services import FollowService

register = template.Library()

@register.filter
def is_following(user, target_user):
    return user.is_following(target_user)

@register.simple_tag
def follow_button(user, target_account):
    follow_service = FollowService()
    is_following = follow_service.is_following(user.id, target_account.id)

    return render_to_string('tags/follow_button.html', {
        'user': user,
        'target_account': target_account,
        'is_following': is_following
    })