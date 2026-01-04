from django.db import models
from django.contrib.auth.models import User

# ------------------------------
# Resume model (main)
# ------------------------------
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # allow multiple resumes per user
    full_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=200, null=True, blank=True)  # e.g., "Software Engineer"
    email = models.EmailField()
    mobile = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Hyderabad, Telangana"
    linkedin_url = models.URLField(max_length=300, null=True, blank=True)
    github_url = models.URLField(max_length=300, null=True, blank=True)
    portfolio_url = models.URLField(max_length=300, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)  # Career objective
    professional_summary = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)  # comma-separated or JSON list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


# ------------------------------
# Education model
# ------------------------------
class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="educations")
    degree = models.CharField(max_length=200)
    branch = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=10)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


# ------------------------------
# Project model (max 2 per resume)
# ------------------------------
class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


# ------------------------------
# Skills model (optional if separate)
# ------------------------------
class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills_list")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ------------------------------
# Work Experience model
# ------------------------------
class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="work_experiences")
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=50)  # e.g., "Jan 2025" or "2023"
    end_date = models.CharField(max_length=50, null=True, blank=True)  # "Present" or "Mar 2024"
    description = models.TextField()  # Bullet points of responsibilities
    order = models.IntegerField(default=0)  # For ordering experiences

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.position} at {self.company_name}"


# ------------------------------
# Certification model
# ------------------------------
class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=300)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=50, null=True, blank=True)
    credential_id = models.CharField(max_length=100, null=True, blank=True)
    credential_url = models.URLField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


# ------------------------------
# Extra-Curricular Activity model
# ------------------------------
class ExtraCurricular(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="extra_curriculars")
    organization = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=50, null=True, blank=True)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.role} at {self.organization}"


# ------------------------------
# Honours and Achievement model
# ------------------------------
class Achievement(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


# ------------------------------
# Job Description model for ATS
# ------------------------------
class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="job_descriptions")
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


