from logging import DEBUG
from django import template

register = template.Library()

@register.simple_tag
def build_https_absolute_uri(request):
    print("変更")
    if DEBUG:
        return request.build_absolute_uri()
    
    url = request.build_absolute_uri()
    return url.replace("http://", "https://")

@register.simple_tag
def convert_https(content):
    if DEBUG:
        return content
    return content.replace("http://", "https://")