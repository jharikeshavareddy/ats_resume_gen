from django.contrib import admin
from .models import (Resume, Education, Project, Skill, JobDescription,
                     WorkExperience, Certification, ExtraCurricular, Achievement)

# Register your models here.
admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(JobDescription)
admin.site.register(WorkExperience)
admin.site.register(Certification)
admin.site.register(ExtraCurricular)
admin.site.register(Achievement)
