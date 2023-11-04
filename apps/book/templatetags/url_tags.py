from django import template

register = template.Library()

@register.simple_tag
def build_https_absolute_uri(request):
    url = request.build_absolute_uri()
    return url.replace("http://", "https://")
