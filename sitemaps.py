# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from blog.models import BlogPost
from home.models import Project, ProjectCategory

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ['home', 'about', 'projects', 'blog',]

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        # For static pages, return a fixed recent date
        return timezone.now() - timedelta(days=7)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Project.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at


class ProjectCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ProjectCategory.objects.all()
    
    def lastmod(self, obj):
        latest_project = obj.project_set.filter(is_active=True).order_by('-updated_at').first()
        return latest_project.updated_at if latest_project else timezone.now()


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return BlogPost.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at


# Configure sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'project_categories': ProjectCategorySitemap,
    'blog': BlogSitemap,
}