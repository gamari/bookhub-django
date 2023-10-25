import logging

from django import template
from django.template.loader import render_to_string

from apps.follow.domain.services import FollowService

logger = logging.getLogger("app_logger")

register = template.Library()

@register.filter
def is_following(user, target_user):
    return user.is_following(target_user)

@register.simple_tag
def follow_button(user, target):
    follow_service = FollowService()
    is_following = follow_service.is_following(user.id, target.id)
    is_self = user.id == target.id
    
    logger.debug(user.id)
    logger.debug(target.id)
    logger.debug(is_self)

    return render_to_string('tags/follow_button.html', {
        'user': user,
        'target_account': target,
        'is_following': is_following,
        'is_self': is_self,
        "is_authenticated": user.is_authenticated,
    })