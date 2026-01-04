"""
PDF Resume Generator using ReportLab
Generates professional PDF resumes matching the preview design
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


def add_section_header(elements, title, heading_style):
    """Helper function to add a section header with underline"""
    elements.append(Paragraph(title, heading_style))
    # Add a colored horizontal line
    hr = HRFlowable(
        width="100%",
        thickness=2,
        color=colors.HexColor('#667eea'),
        spaceBefore=2,
        spaceAfter=10
    )
    elements.append(hr)


def generate_pdf_resume(resume):
    """
    Generate a PDF resume using ReportLab
    
    Args:
        resume: Resume model instance with all related data
        
    Returns:
        BytesIO: PDF file content
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#667eea'),
        borderPadding=0,
        borderRadius=0,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    bold_style = ParagraphStyle(
        'CustomBold',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )
    
    # Header - Name
    elements.append(Paragraph(resume.full_name.upper(), title_style))
    
    # Job Title
    if resume.job_title:
        elements.append(Paragraph(resume.job_title, subtitle_style))
    
    # Contact Information with Unicode symbols
    contact_parts = []
    if resume.location:
        contact_parts.append(f"📍 {resume.location}")
    if resume.mobile:
        contact_parts.append(f"📞 {resume.mobile}")
    contact_parts.append(f"✉️ {resume.email}")
    
    contact_text = " • ".join(contact_parts)
    elements.append(Paragraph(contact_text, contact_style))
    
    # Social Links with symbols
    if resume.linkedin_url or resume.github_url or resume.portfolio_url:
        social_parts = []
        if resume.linkedin_url:
            social_parts.append(f'🔗 <a href="{resume.linkedin_url}" color="blue">LinkedIn</a>')
        if resume.github_url:
            social_parts.append(f'💻 <a href="{resume.github_url}" color="blue">GitHub</a>')
        if resume.portfolio_url:
            social_parts.append(f'🌐 <a href="{resume.portfolio_url}" color="blue">Portfolio</a>')
        
        social_text = " • ".join(social_parts)
        elements.append(Paragraph(social_text, contact_style))
    
    # Add a line separator
    elements.append(Spacer(1, 0.1*inch))
    
    # Objective
    if resume.objective:
        add_section_header(elements, "🎯 OBJECTIVE", heading_style)
        elements.append(Paragraph(resume.objective, normal_style))
        elements.append(Spacer(1, 0.15*inch))
    
    # Professional Summary
    if resume.professional_summary:
        add_section_header(elements, "👤 PROFESSIONAL SUMMARY", heading_style)
        elements.append(Paragraph(resume.professional_summary, normal_style))
        elements.append(Spacer(1, 0.15*inch))
    
    # Work Experience
    work_experiences = resume.work_experiences.all().order_by('-order', '-id')
    if work_experiences.exists():
        add_section_header(elements, "💼 WORK EXPERIENCE", heading_style)
        for exp in work_experiences:
            # Position and Company
            exp_header = f"<b>{exp.position}</b> - {exp.company_name}"
            if exp.location:
                exp_header += f" • {exp.location}"
            elements.append(Paragraph(exp_header, bold_style))
            
            # Dates
            date_range = exp.start_date
            if exp.end_date:
                date_range += f" - {exp.end_date}"
            elements.append(Paragraph(f"<i>{date_range}</i>", normal_style))
            
            # Description
            if exp.description:
                for line in exp.description.strip().split('\n'):
                    line = line.strip()
                    if line:
                        line = line.lstrip('•-*').strip()
                        elements.append(Paragraph(f"• {line}", normal_style))
            
            elements.append(Spacer(1, 0.1*inch))
    
    # Education
    educations = resume.educations.all()
    if educations.exists():
        add_section_header(elements, "🎓 EDUCATION", heading_style)
        for edu in educations:
            degree_text = edu.degree
            if edu.branch:
                degree_text += f" in {edu.branch}"
            elements.append(Paragraph(f"<b>{degree_text}</b>", bold_style))
            elements.append(Paragraph(f"{edu.institution} - {edu.year}", normal_style))
            elements.append(Spacer(1, 0.05*inch))
        elements.append(Spacer(1, 0.1*inch))
    
    # Projects
    projects = resume.projects.all()
    if projects.exists():
        add_section_header(elements, "🚀 PROJECTS", heading_style)
        for project in projects:
            elements.append(Paragraph(f"<b>{project.title}</b>", bold_style))
            if project.description:
                for line in project.description.strip().split('\n'):
                    line = line.strip()
                    if line:
                        line = line.lstrip('•-*').strip()
                        elements.append(Paragraph(f"• {line}", normal_style))
            elements.append(Spacer(1, 0.1*inch))
    
    # Technical Skills
    skills_list = []
    skill_objs = resume.skills_list.all()
    if skill_objs.exists():
        skills_list = [s.name for s in skill_objs]
    elif resume.skills:
        skills_list = [s.strip() for s in resume.skills.split(",") if s.strip()]
    
    if skills_list:
        add_section_header(elements, "💻 TECHNICAL SKILLS", heading_style)
        # Format skills as badges
        skills_text = " • ".join(skills_list)
        elements.append(Paragraph(skills_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Certifications
    certifications = resume.certifications.all()
    if certifications.exists():
        add_section_header(elements, "🏆 CERTIFICATIONS", heading_style)
        for cert in certifications:
            cert_text = f"<b>{cert.name}</b> - {cert.issuing_organization}"
            if cert.issue_date:
                cert_text += f" ({cert.issue_date})"
            elements.append(Paragraph(cert_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Extra-Curricular Activities
    extra_curriculars = resume.extra_curriculars.all()
    if extra_curriculars.exists():
        add_section_header(elements, "👥 EXTRA-CURRICULAR ACTIVITIES", heading_style)
        for activity in extra_curriculars:
            activity_header = f"<b>{activity.role}</b> - {activity.organization}"
            if activity.location:
                activity_header += f" • {activity.location}"
            elements.append(Paragraph(activity_header, bold_style))
            
            if activity.start_date:
                date_range = activity.start_date
                if activity.end_date:
                    date_range += f" - {activity.end_date}"
                elements.append(Paragraph(f"<i>{date_range}</i>", normal_style))
            
            if activity.description:
                for line in activity.description.strip().split('\n'):
                    line = line.strip()
                    if line:
                        line = line.lstrip('•-*').strip()
                        elements.append(Paragraph(f"• {line}", normal_style))
            
            elements.append(Spacer(1, 0.1*inch))
    
    # Honours and Achievements
    achievements = resume.achievements.all()
    if achievements.exists():
        add_section_header(elements, "🏅 HONOURS AND ACHIEVEMENTS", heading_style)
        for achievement in achievements:
            achievement_text = f"<b>{achievement.title}</b>"
            if achievement.description:
                achievement_text += f": {achievement.description}"
            elements.append(Paragraph(achievement_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
