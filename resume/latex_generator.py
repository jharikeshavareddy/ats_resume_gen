"""
LaTeX Resume Generator
Generates a professional LaTeX resume from Resume model data
"""

def escape_latex(text):
    """Escape special LaTeX characters"""
    if not text:
        return ""
    
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generate_latex_resume(resume):
    """
    Generate LaTeX code for a resume
    
    Args:
        resume: Resume model instance with all related data
        
    Returns:
        str: Complete LaTeX document as string
    """
    
    # Get related data
    educations = resume.educations.all()
    work_experiences = resume.work_experiences.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    extra_curriculars = resume.extra_curriculars.all()
    achievements = resume.achievements.all()
    
    # Build skills list
    skills_list = []
    skill_objs = resume.skills_list.all()
    if skill_objs.exists():
        skills_list = [s.name for s in skill_objs]
    elif resume.skills:
        skills_list = [s.strip() for s in resume.skills.split(",") if s.strip()]
    
    # Start building LaTeX document
    latex_content = r"""%-------------------------
% Resume in Latex
% Auto-generated from ATS Resume System
%------------------------

\documentclass[letterpaper,10pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage[dvipsnames]{xcolor}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage{multicol}
\setlength{\multicolsep}{-3.0pt}
\setlength{\columnsep}{-1pt}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.55in}
\addtolength{\evensidemargin}{-0.4in}
\addtolength{\textwidth}{0.95in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.3in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-3pt}\color{BrickRed}\scshape\raggedright\normalsize\bfseries
}{}{0em}{}[\color{BrickRed}\titlerule \vspace{-4pt}]

\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\footnotesize{{#1 \vspace{-1pt}}}
}
\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & \textbf{\footnotesize #2} \\
      \textit{\footnotesize#3} & \textit{\footnotesize #4} \\
    \end{tabular*}\vspace{-5pt}
}
\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.98\textwidth}{l@{\extracolsep{\fill}}r}
      \footnotesize#1 & \textbf{\footnotesize #2}\\
    \end{tabular*}\vspace{-5pt}
}
\renewcommand\labelitemi{$\vcenter{\hbox{\tiny$\bullet$}}$}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-3pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

\vspace*{-10pt}
\begin{center}
"""
    
    # Header with name and contact info
    latex_content += f"  {{\\LARGE \\scshape {escape_latex(resume.full_name.upper())}}} \\\\ \\vspace{{3pt}}\n"
    
    if resume.job_title:
        latex_content += f"  \\footnotesize {escape_latex(resume.job_title)} \\\\ \\vspace{{2pt}}\n"
    
    # Contact information
    contact_parts = []
    if resume.location:
        contact_parts.append(f"\\footnotesize {escape_latex(resume.location)}")
    if resume.mobile:
        contact_parts.append(f"\\raisebox{{-0.1\\height}}\\faPhone\\ {escape_latex(resume.mobile)}")
    
    if contact_parts:
        latex_content += "  " + " ~ \n  ".join(contact_parts) + " ~\n"
    
    # Email and social links
    social_links = []
    if resume.email:
        social_links.append(f"\\href{{mailto:{escape_latex(resume.email)}}}{{\\raisebox{{-0.2\\height}}\\faEnvelope\\  \\underline{{{escape_latex(resume.email)}}}}}")
    if resume.linkedin_url:
        social_links.append(f"\\href{{{escape_latex(resume.linkedin_url)}}}{{\\raisebox{{-0.2\\height}}\\faLinkedin\\ \\underline{{LinkedIn}}}}")
    if resume.github_url:
        social_links.append(f"\\href{{{escape_latex(resume.github_url)}}}{{\\raisebox{{-0.2\\height}}\\faGithub\\ \\underline{{GitHub}}}}")
    
    if social_links:
        latex_content += "  " + " ~\n  ".join(social_links) + "\n"
    
    latex_content += "  \\vspace{-6pt}\n\\end{center}\n\n"
    
    # Objective section
    if resume.objective:
        latex_content += "%-----------OBJECTIVE-----------\n"
        latex_content += "\\section{Objective}\n"
        latex_content += "\\begin{flushleft}\n"
        latex_content += f"\\footnotesize {escape_latex(resume.objective)}\n"
        latex_content += "\\end{flushleft}\n\n"
    
    # Education section
    if educations.exists():
        latex_content += "%-----------EDUCATION-----------\n"
        latex_content += "\\section{Education}\n"
        latex_content += "\\resumeSubHeadingListStart\n"
        
        for edu in educations:
            institution = escape_latex(edu.institution)
            year = escape_latex(edu.year)
            degree = escape_latex(edu.degree)
            branch = escape_latex(edu.branch) if edu.branch else ""
            
            if branch:
                degree_text = f"{degree} in {branch}"
            else:
                degree_text = degree
            
            latex_content += f"\\resumeSubheading\n"
            latex_content += f"{{{institution}}}{{{year}}}\n"
            latex_content += f"{{{degree_text}}}{{}}\n"
        
        latex_content += "\\resumeSubHeadingListEnd\n\n"
    
    # Work Experience section
    if work_experiences.exists():
        latex_content += "%-----------EXPERIENCE-----------\n"
        latex_content += "\\section{Work Experience}\n"
        latex_content += "\\resumeSubHeadingListStart\n\n"
        
        for exp in work_experiences:
            company = escape_latex(exp.company_name)
            position = escape_latex(exp.position)
            location = escape_latex(exp.location) if exp.location else "Remote"
            
            # Date range
            date_range = escape_latex(exp.start_date)
            if exp.end_date:
                date_range += f" -- {escape_latex(exp.end_date)}"
            
            latex_content += f"\\resumeSubheading\n"
            latex_content += f"{{{company}}}{{{date_range}}}\n"
            latex_content += f"{{{position}}}{{{location}}}\n"
            
            # Description as bullet points
            if exp.description:
                latex_content += "\\resumeItemListStart\n"
                # Split description by newlines or bullet points
                desc_lines = exp.description.strip().split('\n')
                for line in desc_lines:
                    line = line.strip()
                    if line:
                        # Remove existing bullet points if any
                        line = line.lstrip('•-*').strip()
                        latex_content += f"\\resumeItem{{{escape_latex(line)}}}\n"
                latex_content += "\\resumeItemListEnd\n"
            
            latex_content += "\n"
        
        latex_content += "\\resumeSubHeadingListEnd\n\n"
    
    # Projects section
    if projects.exists():
        latex_content += "%-----------PROJECTS-----------\n"
        latex_content += "\\section{Projects}\n"
        latex_content += "\\resumeSubHeadingListStart\n\n"
        
        for project in projects:
            title = escape_latex(project.title)
            latex_content += f"\\resumeProjectHeading{{\\textbf{{{title}}}}}{{}}\n"
            
            if project.description:
                latex_content += "\\resumeItemListStart\n"
                desc_lines = project.description.strip().split('\n')
                for line in desc_lines:
                    line = line.strip()
                    if line:
                        line = line.lstrip('•-*').strip()
                        latex_content += f"\\resumeItem{{{escape_latex(line)}}}\n"
                latex_content += "\\resumeItemListEnd\n"
            
            latex_content += "\n\\vspace{-8pt}\n"
        
        latex_content += "\\resumeSubHeadingListEnd\n\n"
    
    # Technical Skills section
    if skills_list:
        latex_content += "%-----------TECHNICAL SKILLS-----------\n"
        latex_content += "\\section{Technical Skills}\n"
        latex_content += "\\begin{itemize}[leftmargin=0.15in, label={}]\n"
        latex_content += "  \\item{\n"
        latex_content += "        \\footnotesize\n"
        
        # Group skills by category if possible (you can enhance this)
        skills_text = ", ".join([escape_latex(skill) for skill in skills_list])
        latex_content += f"        \\textbf{{Skills:}} {skills_text}\n"
        
        latex_content += "        }\n"
        latex_content += "\\end{itemize}\n\n"
    
    # Certifications section
    if certifications.exists():
        latex_content += "%-----------CERTIFICATIONS-----------\n"
        latex_content += "\\section{Certifications}\n"
        latex_content += "\\resumeItemListStart\n"
        
        for cert in certifications:
            cert_text = f"{escape_latex(cert.name)} — {escape_latex(cert.issuing_organization)}"
            latex_content += f"\\resumeItem{{{cert_text}}}\n"
        
        latex_content += "\\resumeItemListEnd\n\n"
    
    # Extra-Curricular Activities section
    if extra_curriculars.exists():
        latex_content += "%-----------EXTRA-CURRICULAR-----------\n"
        latex_content += "\\section{Extra-Curricular Activities}\n"
        latex_content += "\\resumeSubHeadingListStart\n\n"
        
        for activity in extra_curriculars:
            org = escape_latex(activity.organization)
            role = escape_latex(activity.role)
            location = escape_latex(activity.location) if activity.location else ""
            
            date_range = ""
            if activity.start_date:
                date_range = escape_latex(activity.start_date)
                if activity.end_date:
                    date_range += f" -- {escape_latex(activity.end_date)}"
            
            latex_content += f"\\resumeSubheading\n"
            latex_content += f"{{{role}, {org}}}{{{date_range}}}\n"
            latex_content += f"{{}}{{{location}}}\n"
            
            if activity.description:
                latex_content += "\\resumeItemListStart\n"
                desc_lines = activity.description.strip().split('\n')
                for line in desc_lines:
                    line = line.strip()
                    if line:
                        line = line.lstrip('•-*').strip()
                        latex_content += f"\\resumeItem{{{escape_latex(line)}}}\n"
                latex_content += "\\resumeItemListEnd\n"
        
        latex_content += "\\resumeSubHeadingListEnd\n\n"
    
    # Honours and Achievements section
    if achievements.exists():
        latex_content += "%-----------HONOURS AND AWARDS-----------\n"
        latex_content += "\\section{Honours and Achievements}\n"
        latex_content += "\\resumeItemListStart\n"
        
        for achievement in achievements:
            achievement_text = escape_latex(achievement.title)
            if achievement.description:
                achievement_text += f": {escape_latex(achievement.description)}"
            latex_content += f"\\resumeItem{{{achievement_text}}}\n"
        
        latex_content += "\\resumeItemListEnd\n\n"
    
    # End document
    latex_content += "\\end{document}\n"
    
    return latex_content
