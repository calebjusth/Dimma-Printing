from django.shortcuts import render

from blog.models import BlogPost
from .models import *
# views.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.template.context_processors import csrf
# Create your views here.

def home(request):
    clients = Client.objects.all()
    projects = Project.objects.filter(is_featured=True)[:5]
    latest_blogs = BlogPost.published.all()[:3]


    context = {
        'clients': clients,
        'projects': projects,
        'latest_blogs': latest_blogs,


    }

    return render(request, './home/home.html', context)


def about(request):
    # Get or create default instances
    hero = HeroSection.objects.first()
    if not hero:
        hero = HeroSection.objects.create()
    
    cta = CTASection.objects.first()
    if not cta:
        cta = CTASection.objects.create()
    
    context = {
        'hero': hero,
        'companies': SisterCompany.objects.filter(is_active=True).order_by('order'),  
        'timeline_events': TimelineEvent.objects.filter(is_active=True).order_by('order'),
        'values': CompanyValue.objects.filter(is_active=True).order_by('order'),
        'cta': cta,
    }
    return render(request, './home/about.html', context)



def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)



@staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def edit_section(request, section_name):
    if request.method == 'GET':
        # Return form for the requested section
        if section_name == 'hero':
            instance = HeroSection.objects.first()
            if not instance:
                instance = HeroSection.objects.create()
            form = HeroSectionForm(instance=instance)
            
        elif section_name == 'sister-companies':
            # This will be handled differently - we'll return a list of companies
            companies = SisterCompany.objects.filter(is_active=True).order_by('order')
            data = {
                'type': 'list',
                'items': [{'id': c.id, 'name': c.name} for c in companies]
            }
            return JsonResponse(data)
            
        elif section_name == 'timeline':
            events = TimelineEvent.objects.filter(is_active=True).order_by('order')
            data = {
                'type': 'list',
                'items': [{'id': e.id, 'title': e.title} for e in events]
            }
            return JsonResponse(data)
            
        elif section_name == 'values':
            values = CompanyValue.objects.filter(is_active=True).order_by('order')
            data = {
                'type': 'list',
                'items': [{'id': v.id, 'title': v.title} for v in values]
            }
            return JsonResponse(data)
            
        elif section_name == 'cta':
            instance = CTASection.objects.first()
            if not instance:
                instance = CTASection.objects.create()
            form = CTASectionForm(instance=instance)
            
        else:
            return JsonResponse({'error': 'Invalid section'}, status=400)
        
        # Add CSRF token to context and render form as HTML
        context = {'form': form, 'section': section_name}
        context.update(csrf(request))  # Add CSRF token to context
        form_html = render_to_string('./home/partials/edit_form.html', context)
        return JsonResponse({'form': form_html})
    
    else:  # POST - save data
        try:
            # Handle FormData instead of JSON
            if section_name == 'hero':
                instance = HeroSection.objects.first()
                if not instance:
                    instance = HeroSection.objects.create()
                form = HeroSectionForm(request.POST, request.FILES, instance=instance)
                
            elif section_name == 'cta':
                instance = CTASection.objects.first()
                if not instance:
                    instance = CTASection.objects.create()
                form = CTASectionForm(request.POST, instance=instance)
                
            else:
                return JsonResponse({'error': 'Invalid section for POST'}, status=400)
            
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'errors': form.errors}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def edit_list_item(request, section_name, item_id=None):
    # Map section names to models and forms
    section_map = {
        'sister-companies': (SisterCompany, SisterCompanyForm),
        'timeline': (TimelineEvent, TimelineEventForm),
        'values': (CompanyValue, CompanyValueForm),
    }
    
    if section_name not in section_map:
        return JsonResponse({'error': 'Invalid section'}, status=400)
    
    ModelClass, FormClass = section_map[section_name]
    
    if request.method == 'GET':
        # Return form for editing or creating
        if item_id:
            item = get_object_or_404(ModelClass, id=item_id)
            form = FormClass(instance=item)
        else:
            form = FormClass()
        
        context = {'form': form, 'section': section_name}
        context.update(csrf(request))
        form_html = render_to_string('./home/partials/edit_form.html', context)
        return JsonResponse({'form': form_html})
    
    elif request.method == 'POST':
        # Handle form submission
        if item_id:
            item = get_object_or_404(ModelClass, id=item_id)
            form = FormClass(request.POST, instance=item)
        else:
            form = FormClass(request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    elif request.method == 'DELETE':
        if not item_id:
            return JsonResponse({'error': 'Item ID required for deletion'}, status=400)
        
        item = get_object_or_404(ModelClass, id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    




def projects(request):
    categories = ProjectCategory.objects.all()
    projects = Project.objects.all().select_related('category', 'client')
    
    context = {
        'categories': categories,
        'projects': projects,
    }
    return render(request, './home/projects.html', context)