from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from docx import Document
import subprocess
import os
import tempfile

from .models import (Resume, Education, Project, Skill, JobDescription,
                     WorkExperience, Certification, ExtraCurricular, Achievement)
from .ats_engine import ats_score, missing_keywords
from .forms import RegisterForm
from .latex_generator import generate_latex_resume


# ---------------- AUTH ---------------- #
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "resume/register.html", {"form": form})


def login_views(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "resume/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- DASHBOARD ---------------- #
@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by("-created_at")
    jobs = JobDescription.objects.filter(user=request.user).order_by("-created_at")
    
    # Calculate ATS scores for each resume
    resume_scores = []
    for resume in resumes:
        job = JobDescription.objects.filter(resume=resume).first()
        score = ats_score(resume, job) if job else None
        resume_scores.append({
            'resume': resume,
            'score': score,
            'has_job': job is not None
        })
    
    return render(request, "resume/dashboard.html", {
        "resumes": resumes,
        "resume_scores": resume_scores,
        "jobs": jobs
    })


# ---------------- CREATE RESUME ---------------- #
@login_required
def create_resume(request):
    if request.method == "POST":

        resume = Resume.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            job_title=request.POST.get("job_title"),
            email=request.POST.get("email"),
            mobile=request.POST.get("mobile"),
            location=request.POST.get("location"),
            linkedin_url=request.POST.get("linkedin_url"),
            github_url=request.POST.get("github_url"),
            portfolio_url=request.POST.get("portfolio_url"),
            objective=request.POST.get("objective"),
            professional_summary=request.POST.get("professional_summary"),
            skills=(request.POST.get("skills") or "").strip(),
        )

        Education.objects.create(
            resume=resume,
            degree=request.POST.get("degree"),
            branch=request.POST.get("branch"),
            institution=request.POST.get("institution"),
            year=request.POST.get("year"),
        )

        Project.objects.create(
            resume=resume,
            title=request.POST.get("project_title"),
            description=request.POST.get("project_description"),
        )

        JobDescription.objects.create(
            user=request.user,
            resume=resume,
            job_title=request.POST.get("job_title"),
            job_description=request.POST.get("job_description"),
        )

        return redirect("resume_preview", resume_id=resume.id)

    return render(request, "resume/create_resume.html")



# ---------------- PREVIEW ---------------- #
@login_required
def resume_preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    job = JobDescription.objects.filter(resume=resume).first()
    score = ats_score(resume, job) if job else 0

    # Build skills list: prefer Skill objects (related_name 'skills_list'),
    # fallback to comma-separated `resume.skills` text field for older data.
    skills_list = []
    # If there are Skill instances related to this resume, use them.
    skill_objs = resume.skills_list.all()
    if skill_objs.exists():
        skills_list = [s.name for s in skill_objs]
    else:
        if resume.skills:
            skills_list = [s.strip() for s in resume.skills.split(",") if s.strip()]

    # Get role-specific recommendations if job description exists
    from .ats_engine import get_role_recommendations, missing_keywords as get_missing_keywords
    role_recommendations = None
    missing_kw = []
    detected_role = None
    
    if job:
        role_recommendations = get_role_recommendations(job)
        missing_kw = get_missing_keywords(resume, job)
        if role_recommendations:
            detected_role = role_recommendations['role']
    
    return render(request, "resume/resume_preview.html", {
        "resume": resume,
        "educations": resume.educations.all(),
        "work_experiences": resume.work_experiences.all(),
        "projects": resume.projects.all(),
        "certifications": resume.certifications.all(),
        "extra_curriculars": resume.extra_curriculars.all(),
        "achievements": resume.achievements.all(),
        "skills_list": skills_list,  
        "score": score,
        "detected_role": detected_role,
        "role_recommendations": role_recommendations,
        "missing_keywords": missing_kw[:10],  # Top 10 missing keywords
    })




# ---------------- EXPORT DOCX ---------------- #
@login_required
def export_resume_docx(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    job = JobDescription.objects.filter(resume=resume).first()
    score = ats_score(resume, job) if job else 0

    doc = Document()
    doc.add_heading(resume.full_name.upper(), level=1)
    doc.add_paragraph(resume.email)
    doc.add_paragraph(resume.mobile)

    doc.add_heading("Professional Summary", level=2)
    doc.add_paragraph(resume.professional_summary or "")

    doc.add_heading("Education", level=2)
    for edu in resume.educations.all():
        doc.add_paragraph(f"{edu.degree} - {edu.institution} ({edu.year})")

    doc.add_heading("Projects", level=2)
    for project in resume.projects.all()[:2]:
        doc.add_paragraph(f"{project.title}: {project.description}")

    doc.add_heading("Skills", level=2)
    # Export skills: prefer Skill objects, fallback to resume.skills text
    skill_objs = resume.skills_list.all()
    if skill_objs.exists():
        doc.add_paragraph(', '.join([s.name for s in skill_objs]))
    else:
        doc.add_paragraph(resume.skills or "")

    doc.add_paragraph(f"\nATS SCORE: {score}%")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{resume.full_name}.docx"'
    doc.save(response)
    return response


# ---------------- EDIT RESUME ---------------- #
@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        # Update basic resume info
        resume.full_name = request.POST.get("full_name")
        resume.job_title = request.POST.get("job_title")
        resume.email = request.POST.get("email")
        resume.mobile = request.POST.get("mobile")
        resume.location = request.POST.get("location")
        resume.linkedin_url = request.POST.get("linkedin_url")
        resume.github_url = request.POST.get("github_url")
        resume.portfolio_url = request.POST.get("portfolio_url")
        resume.objective = request.POST.get("objective")
        resume.professional_summary = request.POST.get("professional_summary")
        resume.skills = request.POST.get("skills")
        resume.save()
        
        return redirect("resume_preview", resume_id=resume.id)
    
    # Get all related data for editing
    context = {
        "resume": resume,
        "educations": resume.educations.all(),
        "work_experiences": resume.work_experiences.all(),
        "projects": resume.projects.all(),
        "certifications": resume.certifications.all(),
        "extra_curriculars": resume.extra_curriculars.all(),
        "achievements": resume.achievements.all(),
    }
    
    return render(request, "resume/edit_resume.html", context)


# ---------------- MANAGE EDUCATION ---------------- #
@login_required
def add_education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        Education.objects.create(
            resume=resume,
            degree=request.POST.get("degree"),
            branch=request.POST.get("branch"),
            institution=request.POST.get("institution"),
            year=request.POST.get("year"),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_education.html", {"resume": resume})


@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, resume__user=request.user)
    resume_id = education.resume.id
    education.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- MANAGE WORK EXPERIENCE ---------------- #
@login_required
def add_work_experience(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        WorkExperience.objects.create(
            resume=resume,
            company_name=request.POST.get("company_name"),
            position=request.POST.get("position"),
            location=request.POST.get("location"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            description=request.POST.get("description"),
            order=request.POST.get("order", 0),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_work_experience.html", {"resume": resume})


@login_required
def delete_work_experience(request, experience_id):
    experience = get_object_or_404(WorkExperience, id=experience_id, resume__user=request.user)
    resume_id = experience.resume.id
    experience.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- MANAGE PROJECTS ---------------- #
@login_required
def add_project(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        Project.objects.create(
            resume=resume,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_project.html", {"resume": resume})


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, resume__user=request.user)
    resume_id = project.resume.id
    project.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- MANAGE CERTIFICATIONS ---------------- #
@login_required
def add_certification(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        Certification.objects.create(
            resume=resume,
            name=request.POST.get("name"),
            issuing_organization=request.POST.get("issuing_organization"),
            issue_date=request.POST.get("issue_date"),
            credential_id=request.POST.get("credential_id"),
            credential_url=request.POST.get("credential_url"),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_certification.html", {"resume": resume})


@login_required
def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id, resume__user=request.user)
    resume_id = certification.resume.id
    certification.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- MANAGE EXTRA-CURRICULAR ---------------- #
@login_required
def add_extra_curricular(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        ExtraCurricular.objects.create(
            resume=resume,
            organization=request.POST.get("organization"),
            role=request.POST.get("role"),
            location=request.POST.get("location"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            description=request.POST.get("description"),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_extra_curricular.html", {"resume": resume})


@login_required
def delete_extra_curricular(request, extra_curricular_id):
    extra_curricular = get_object_or_404(ExtraCurricular, id=extra_curricular_id, resume__user=request.user)
    resume_id = extra_curricular.resume.id
    extra_curricular.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- MANAGE ACHIEVEMENTS ---------------- #
@login_required
def add_achievement(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == "POST":
        Achievement.objects.create(
            resume=resume,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            date=request.POST.get("date"),
        )
        return redirect("edit_resume", resume_id=resume.id)
    
    return render(request, "resume/add_achievement.html", {"resume": resume})


@login_required
def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id, resume__user=request.user)
    resume_id = achievement.resume.id
    achievement.delete()
    return redirect("edit_resume", resume_id=resume_id)


# ---------------- EXPORT LATEX/PDF ---------------- #
@login_required
def export_resume_latex(request, resume_id):
    """Export resume as LaTeX source file"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    latex_content = generate_latex_resume(resume)
    
    response = HttpResponse(content_type="application/x-latex")
    response["Content-Disposition"] = f'attachment; filename="{resume.full_name}_resume.tex"'
    response.write(latex_content)
    
    return response


@login_required
def export_resume_pdf(request, resume_id):
    """Export resume as PDF using ReportLab"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    from .pdf_generator import generate_pdf_resume
    
    try:
        pdf_content = generate_pdf_resume(resume)
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
        return response
    
    except Exception as e:
        return HttpResponse(
            f"PDF generation failed: {str(e)}. Please try downloading DOCX or LaTeX instead.",
            status=500
        )
