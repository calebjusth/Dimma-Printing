# social_media_tags.py
from django import template
from ..models import SocialMedia

register = template.Library()

@register.simple_tag
def get_social_media_links():
    return SocialMedia.objects.filter(is_active=True)