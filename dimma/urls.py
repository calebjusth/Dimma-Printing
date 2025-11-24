
from django.contrib import admin
from django.urls import include, path
from . import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])