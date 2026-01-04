from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Resume, JobDescription, Education, Project, Skill


# ------------------------------
# User Registration Form
# ------------------------------
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# ------------------------------
# Resume Form
# ------------------------------
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'job_title', 'email', 'mobile', 'location', 
                  'linkedin_url', 'github_url', 'portfolio_url', 
                  'objective', 'professional_summary', 'skills']
        widgets = {
            'objective': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Your career objective'
            }),
            'professional_summary': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write a brief summary about yourself'
            }),
            'skills': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Python, Django, SQL...'
            }),
        }


# ------------------------------
# Education Form
# ------------------------------
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'branch', 'institution', 'year']

# ------------------------------
# Project Form (max 2 per resume)
# ------------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe your project in detail'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Safely get resume
        resume = getattr(self.instance, 'resume', None) or self.initial.get('resume')
        if resume:
            existing_projects = Project.objects.filter(resume=resume)
            # Exclude current instance if updating
            if self.instance.pk:
                existing_projects = existing_projects.exclude(pk=self.instance.pk)
            if existing_projects.count() >= 2:
                raise forms.ValidationError("Maximum 2 projects are allowed per resume.")
        return cleaned_data


# ------------------------------
# Skill Form
# ------------------------------
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Python, Django, SQL...'})
        }


# ------------------------------
# Job Description Form
# ------------------------------
class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['job_title', 'job_description']
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python Full Stack Developer'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Paste the job description here...'
            }),
        }
