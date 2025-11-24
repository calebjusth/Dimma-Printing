# models.py
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='clients/logos/')

    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
    def __str__(self):
        return self.name

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = [ 'name']
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('both', 'Both Image and Video'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='projects/images/', blank=True, null=True)
    video = models.FileField(
        upload_to="videos/", 
        blank=True, 
        null=True, 
        help_text="Upload a video file (MP4, AVI, MOV, etc.)"
    )

    testimonial = models.TextField(blank=True, help_text="Client testimonial about this project")
    testimonial_author = models.CharField(max_length=100, blank=True)
    testimonial_author_position = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = [ '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def clean(self):
        if self.project_type == 'image' and not self.image:
            raise ValidationError({'image': 'Image is required for image projects.'})
        if self.project_type == 'video' and not self.video_url:
            raise ValidationError({'video': 'Video URL is required for video projects.'})
        if self.project_type == 'both' and (not self.image or not self.video):
            raise ValidationError({
                'image': 'Image is required for projects with both image and video.',
                'video': 'Video URL is required for projects with both image and video.'
            })
    
    def __str__(self):
        return self.title

class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('telegram', 'Telegram'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
        ('pinterest', 'Pinterest'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS class for the icon (if using icon fonts)")
    is_active = models.BooleanField(default=True)

    
    class Meta:
        ordering = [ 'platform']
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'
    
    def save(self, *args, **kwargs):
        # Set default icon classes based on platform
        if not self.icon_class:
            icon_map = {
                'facebook': 'fab fa-facebook-f',
                'instagram': 'fab fa-instagram',
                'twitter': 'fab fa-twitter',
                'linkedin': 'fab fa-linkedin-in',
                'youtube': 'fab fa-youtube',
                'telegram': 'fab fa-telegram',
                'tiktok': 'fab fa-tiktok',
                'whatsapp': 'fab fa-whatsapp',
                'pinterest': 'fab fa-pinterest',
            }
            self.icon_class = icon_map.get(self.platform, 'fas fa-link')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_platform_display()}"

class HomeContent(models.Model):
    section = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Home Content'
        verbose_name_plural = 'Home Contents'
    
    def __str__(self):
        return self.section

class Testimonial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='testimonials')
    content = models.TextField()
    author = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = [ '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
    
    def __str__(self):
        return f"Testimonial from {self.author} - {self.client}"

# Additional models you might find useful:

class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    
    class Meta:
        ordering = [ 'title']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = [ 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class ContactInfo(models.Model):
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed code")
    
    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
    
    def __str__(self):
        return "Contact Information"
    



##################################################################################################
                #ABOUT PAGE MODEL DESIGN #
##################################################################################################
class HeroSection(models.Model):
    title_line_1 = models.CharField(max_length=100, default="Our Story of")
    title_line_2 = models.CharField(max_length=100, default="Innovation")
    subtitle = models.TextField(default="Three decades of transforming Ethiopia's printing landscape")
    background_image = models.ImageField(upload_to='about/hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
    
    def __str__(self):
        return "Hero Section Configuration"

class SisterCompany(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.TextField(help_text="Paste SVG code here")  # Alternatively use FileField for SVG upload
    services = models.JSONField(default=list, help_text="List of services as JSON array")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sister Company"
        verbose_name_plural = "Sister Companies"
        ordering = ['order']
    
    def __str__(self):
        return self.name

class TimelineEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.year} - {self.title}"

class CompanyValue(models.Model):
    ICON_CHOICES = [
        ('check', '✓ '),
        ('recycle', '♻ '),
        ('handshake', '🤝'),
        ('clock', '⏱'),
        ('quality', '🏆'),
        ('innovation', '💡'),
    ]
    
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='check')
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Company Value"
        verbose_name_plural = "Company Values"
        ordering = ['order']
    
    def __str__(self):
        return self.title

class CTASection(models.Model):
    title = models.CharField(max_length=200, default="Ready to Bring Your Vision to Life?")
    description = models.TextField(default="Join our family of satisfied clients and experience the Dimma difference")
    button_text = models.CharField(max_length=50, default="Call Us")
    phone_number = models.CharField(max_length=20, default="+251911224244")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "CTA Section"
        verbose_name_plural = "CTA Section"
    
    def __str__(self):
        return "CTA Section Configuration"

# Optional: For section headers and other text content
class ContentSnippet(models.Model):
    key = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    
    class Meta:
        verbose_name = "Content Snippet"
        verbose_name_plural = "Content Snippets"
    
    def __str__(self):
        return self.key