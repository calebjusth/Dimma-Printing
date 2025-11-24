# forms.py
from django import forms
from .models import HeroSection, SisterCompany, TimelineEvent, CompanyValue, CTASection, ContentSnippet

class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = ['title_line_1', 'title_line_2', 'subtitle', 'background_image']
        widgets = {
            'title_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'title_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# forms.py
class SisterCompanyForm(forms.ModelForm):
    services_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="Enter each service on a new line"
    )
    
    class Meta:
        model = SisterCompany
        fields = ['name', 'description', 'icon_svg', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'icon_svg': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.services:
            self.fields['services_text'].initial = '\n'.join(self.instance.services)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        services_text = self.cleaned_data.get('services_text', '')
        instance.services = [service.strip() for service in services_text.split('\n') if service.strip()]
        
        if commit:
            instance.save()
        return instance

class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ['title', 'description', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CompanyValueForm(forms.ModelForm):
    class Meta:
        model = CompanyValue
        fields = ['icon', 'title', 'description', 'order', 'is_active']
        widgets = {
            'icon': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CTASectionForm(forms.ModelForm):
    class Meta:
        model = CTASection
        fields = ['title', 'description', 'button_text', 'phone_number', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContentSnippetForm(forms.ModelForm):
    class Meta:
        model = ContentSnippet
        fields = ['key', 'content']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }