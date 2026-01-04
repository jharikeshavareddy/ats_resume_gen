from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_views, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_resume, name="create"),
    path("preview/<int:resume_id>/", views.resume_preview, name="resume_preview"),
    
    # Edit resume
    path("edit/<int:resume_id>/", views.edit_resume, name="edit_resume"),
    
    # Manage Education
    path("add-education/<int:resume_id>/", views.add_education, name="add_education"),
    path("delete-education/<int:education_id>/", views.delete_education, name="delete_education"),
    
    # Manage Work Experience
    path("add-work-experience/<int:resume_id>/", views.add_work_experience, name="add_work_experience"),
    path("delete-work-experience/<int:experience_id>/", views.delete_work_experience, name="delete_work_experience"),
    
    # Manage Projects
    path("add-project/<int:resume_id>/", views.add_project, name="add_project"),
    path("delete-project/<int:project_id>/", views.delete_project, name="delete_project"),
    
    # Manage Certifications
    path("add-certification/<int:resume_id>/", views.add_certification, name="add_certification"),
    path("delete-certification/<int:certification_id>/", views.delete_certification, name="delete_certification"),
    
    # Manage Extra-Curricular
    path("add-extra-curricular/<int:resume_id>/", views.add_extra_curricular, name="add_extra_curricular"),
    path("delete-extra-curricular/<int:extra_curricular_id>/", views.delete_extra_curricular, name="delete_extra_curricular"),
    
    # Manage Achievements
    path("add-achievement/<int:resume_id>/", views.add_achievement, name="add_achievement"),
    path("delete-achievement/<int:achievement_id>/", views.delete_achievement, name="delete_achievement"),
    
    # Export options
    path("export/docx/<int:resume_id>/", views.export_resume_docx, name="export_docx"),
    path("export/latex/<int:resume_id>/", views.export_resume_latex, name="export_latex"),
    path("export/pdf/<int:resume_id>/", views.export_resume_pdf, name="export_pdf"),
]
