from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import BlogCommentForm
from django.db.models import Count

def blog(request):
    posts = BlogPost.published.all().order_by('-publish_date')
    categories = BlogCategory.objects.annotate(num_posts=Count('blogpost'))
    trending_posts = BlogPost.published.all().order_by('-views')[:3]

    # Get top 15 tags by number of related blog posts
    top_tags = BlogTag.objects.annotate(num_posts=Count('blogposts'))

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, './blog/blog_home.html', {
        'posts': posts,
        'categories': categories,
        'trending_posts': trending_posts,
        'top_tags': top_tags,  # Pass to template
    })


def blog_post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        BlogPost,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
        slug=slug,
        status='published'
    )
    
    # Increment view count
    post.views += 1
    post.save()
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    # Get related posts (same category, excluding current post)
    related_posts = BlogPost.published.filter(
        category=post.category
    ).exclude(
        id=post.id
    ).order_by('-publish_date')[:3]
    
    # If not enough same-category posts, get latest posts
    if len(related_posts) < 3:
        additional_posts = BlogPost.published.exclude(
            id=post.id
        ).exclude(
            id__in=[p.id for p in related_posts]
        ).order_by('-publish_date')[:3-len(related_posts)]
        related_posts = list(related_posts) + list(additional_posts)
    
    # Comment form
    if request.method == 'POST':
        comment_form = BlogCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = BlogCommentForm()  # Reset form after submission
    else:
        comment_form = BlogCommentForm()
    
    return render(request, './blog/blog_post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts, 
    })

def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.published.filter(category=category).order_by('-publish_date')
    categories = BlogCategory.objects.annotate(num_posts=Count('blogpost'))
    
    return render(request, './blog/blog_category.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
    })


def blog_tag(request, slug):
    tag = get_object_or_404(BlogTag, slug=slug)
    posts = BlogPost.published.filter(tags=tag).order_by('-publish_date')
    categories = BlogCategory.objects.annotate(num_posts=Count('blogpost'))
    return render(request, './blog/blog_tag.html', {
        'tag': tag,
        'posts': posts,
        'categories': categories,
    })



