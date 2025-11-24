# admin.py
from django.contrib import admin
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'client', 'project_type', 'is_featured']
    list_filter = ['category', 'project_type', 'is_featured']
    search_fields = ['title', 'description']
    filter_horizontal = []

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active']
    list_editable = [ 'is_active']
    list_filter = ['platform', 'is_active']

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ['section', 'title', 'is_active']
    list_editable = ['is_active']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'client', 'is_featured']
    list_filter = ['is_featured', 'client']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active']
    list_editable = [ 'is_active']



@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one contact info instance
        return not ContactInfo.objects.exists()
    

# admin.py
from django.contrib import admin
from .models import HeroSection, SisterCompany, TimelineEvent, CompanyValue, CTASection, ContentSnippet

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['is_active']
    
    def has_add_permission(self, request):
        # Allow only one instance
        return not HeroSection.objects.exists()



admin.site.register(SisterCompany)