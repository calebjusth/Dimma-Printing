from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('tag/<slug:slug>/', views.blog_tag, name='blog_tag'),
    path('category/<slug:slug>/', views.blog_category, name='blog_category'),
]