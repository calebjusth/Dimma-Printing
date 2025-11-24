from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('projects/', views.projects, name='projects'),

    path('edit-section/<str:section_name>/', views.edit_section, name='edit_section'),
    path('edit-item/<str:section_name>/', views.edit_list_item, name='edit_list_item_new'),
    path('edit-item/<str:section_name>/<int:item_id>/', views.edit_list_item, name='edit_list_item'),
]