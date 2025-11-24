
from .models import HeroSection, SisterCompany, TimelineEvent, CompanyValue, CTASection

def about_page_data(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    if not hero:
        hero = HeroSection.objects.create()
    
    sister_companies = SisterCompany.objects.filter(is_active=True).order_by('order')
    timeline_events = TimelineEvent.objects.filter(is_active=True).order_by('order')
    values = CompanyValue.objects.filter(is_active=True).order_by('order')
    cta = CTASection.objects.filter(is_active=True).first()
    if not cta:
        cta = CTASection.objects.create()
    
    return {
        'about_hero': hero,
        'sister_companies': sister_companies,
        'timeline_events': timeline_events,
        'company_values': values,
        'about_cta': cta,
    }

from django.core.cache import cache
from .models import SocialMedia

def social_media_links(request):
    cache_key = 'social_media_links'
    social_links = cache.get(cache_key)
    
    if not social_links:
        social_links = list(SocialMedia.objects.filter(is_active=True))
        # Cache for 1 hour
        cache.set(cache_key, social_links, 60 * 60)
    
    return {'social_media_links': social_links}