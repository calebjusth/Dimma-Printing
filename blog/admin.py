from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogComment, BlogTag
from django.utils.html import format_html

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish_date', 'status', 'view_count')
    list_filter = ('status', 'publish_date', 'category')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    filter_horizontal = ()

    readonly_fields = ('view_count',)  

    def view_count(self, obj):
        return obj.views
    view_count.short_description = 'Views'

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_date', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug based on name
    ordering = ('name',)
    readonly_fields = ('created_at',)