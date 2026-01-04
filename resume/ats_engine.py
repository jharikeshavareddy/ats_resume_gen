import spacy
import re

nlp = None

# Role-specific keyword mappings
ROLE_KEYWORDS = {
    'full_stack': {
        'core': ['full stack', 'fullstack', 'full-stack', 'frontend', 'backend', 'front-end', 'back-end'],
        'frontend': ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'redux', 'next.js', 'webpack'],
        'backend': ['node.js', 'express', 'django', 'flask', 'spring boot', 'rest api', 'graphql', 'microservices'],
        'database': ['mongodb', 'postgresql', 'mysql', 'sql', 'nosql', 'redis', 'database'],
        'tools': ['git', 'docker', 'kubernetes', 'aws', 'azure', 'ci/cd', 'jenkins']
    },
    'java': {
        'core': ['java', 'j2ee', 'jvm', 'spring', 'spring boot', 'hibernate', 'maven', 'gradle'],
        'frameworks': ['spring mvc', 'spring security', 'spring data', 'jpa', 'jdbc'],
        'tools': ['junit', 'mockito', 'log4j', 'slf4j'],
        'concepts': ['multithreading', 'collections', 'design patterns', 'solid principles']
    },
    'backend': {
        'core': ['backend', 'back-end', 'server-side', 'api', 'rest', 'graphql'],
        'languages': ['python', 'java', 'node.js', 'go', 'ruby', 'php', 'c#', '.net'],
        'frameworks': ['django', 'flask', 'express', 'spring boot', 'fastapi', 'nest.js'],
        'database': ['sql', 'nosql', 'postgresql', 'mongodb', 'mysql', 'redis', 'elasticsearch'],
        'concepts': ['microservices', 'scalability', 'caching', 'message queue', 'kafka', 'rabbitmq']
    },
    'frontend': {
        'core': ['frontend', 'front-end', 'ui', 'ux', 'responsive', 'web development'],
        'frameworks': ['react', 'angular', 'vue', 'next.js', 'nuxt', 'svelte'],
        'languages': ['javascript', 'typescript', 'html', 'css', 'sass', 'scss'],
        'tools': ['webpack', 'babel', 'npm', 'yarn', 'redux', 'mobx', 'tailwind'],
        'concepts': ['spa', 'pwa', 'accessibility', 'performance optimization']
    },
    'react': {
        'core': ['react', 'reactjs', 'react.js', 'jsx', 'hooks', 'components'],
        'ecosystem': ['redux', 'react router', 'next.js', 'gatsby', 'react native'],
        'concepts': ['state management', 'virtual dom', 'lifecycle', 'context api'],
        'tools': ['webpack', 'babel', 'create-react-app', 'vite']
    },
    'python': {
        'core': ['python', 'python3', 'pip', 'virtualenv', 'anaconda'],
        'frameworks': ['django', 'flask', 'fastapi', 'pyramid', 'tornado'],
        'data': ['pandas', 'numpy', 'matplotlib', 'scikit-learn', 'tensorflow', 'pytorch'],
        'tools': ['pytest', 'unittest', 'celery', 'sqlalchemy']
    },
    'devops': {
        'core': ['devops', 'ci/cd', 'automation', 'infrastructure'],
        'tools': ['docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'terraform', 'ansible'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
        'monitoring': ['prometheus', 'grafana', 'elk stack', 'datadog']
    }
}

# ------------------------------
# Load SpaCy model once
# ------------------------------
def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp


# ------------------------------
# Extract keywords from text
# ------------------------------
def extract_keywords(text):
    nlp_model = get_nlp()
    doc = nlp_model(text.lower())
    return {
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop
    }


# ------------------------------
# Detect role from job description
# ------------------------------
def detect_role(job_description):
    """Detect the primary role from job description"""
    jd_lower = job_description.lower()
    
    role_scores = {}
    for role, categories in ROLE_KEYWORDS.items():
        score = 0
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in jd_lower:
                    # Core keywords get higher weight
                    weight = 3 if category == 'core' else 1
                    score += weight
        role_scores[role] = score
    
    # Return role with highest score, or None if no match
    if max(role_scores.values()) > 0:
        return max(role_scores, key=role_scores.get)
    return None

# ------------------------------
# Prepare full resume text dynamically
# ------------------------------
def resume_text(resume):
    text = resume.professional_summary or ""
    text += " " + (resume.objective or "")
    
    # Add skills
    if resume.skills:
        text += " " + resume.skills
    
    # Add work experience
    for exp in resume.work_experiences.all():
        text += f" {exp.position} {exp.company_name} {exp.description}"
    
    # Add project descriptions
    for project in resume.projects.all():
        text += " " + project.title + " " + project.description
    
    # Add education info
    for edu in resume.educations.all():
        text += f" {edu.degree} {edu.branch or ''} {edu.institution} {edu.year}"
    
    # Add certifications
    for cert in resume.certifications.all():
        text += f" {cert.name} {cert.issuing_organization}"
    
    return text.lower()


# ------------------------------
# Calculate ATS score with role-specific analysis
# ------------------------------
def ats_score(resume, job):
    resume_txt = resume_text(resume)
    job_desc = job.job_description.lower()
    
    # Extract keywords using NLP
    r_keywords = extract_keywords(resume_txt)
    j_keywords = extract_keywords(job_desc)
    
    if not j_keywords:
        return 0
    
    # If resume is empty, return 0
    if not r_keywords:
        return 0
    
    # Base keyword matching score
    matched_keywords = r_keywords & j_keywords
    keyword_match = len(matched_keywords) / len(j_keywords)
    base_score = keyword_match * 60  # 60% weight for keyword matching
    
    # Detect role and add role-specific bonus
    role = detect_role(job_desc)
    role_bonus = 0
    
    if role and role in ROLE_KEYWORDS:
        role_keywords = ROLE_KEYWORDS[role]
        total_role_keywords = sum(len(keywords) for keywords in role_keywords.values())
        matched_role_keywords = 0
        
        for category, keywords in role_keywords.items():
            for keyword in keywords:
                if keyword in resume_txt:
                    # Core keywords get higher weight
                    weight = 2 if category == 'core' else 1
                    matched_role_keywords += weight
        
        if total_role_keywords > 0:
            role_bonus = (matched_role_keywords / total_role_keywords) * 40  # 40% weight for role-specific
    
    final_score = base_score + role_bonus
    
    # Add minimum score if there's any match
    if final_score > 0 and final_score < 15:
        final_score = 15  # Minimum 15% if there's any match
    
    return round(min(final_score, 98), 2)  # Cap at 98%


# ------------------------------
# List missing keywords with role-specific suggestions
# ------------------------------
def missing_keywords(resume, job):
    resume_txt = resume_text(resume)
    job_desc = job.job_description.lower()
    
    r_keywords = extract_keywords(resume_txt)
    j_keywords = extract_keywords(job_desc)
    
    missing = list(j_keywords - r_keywords)
    
    # Add role-specific missing keywords
    role = detect_role(job_desc)
    if role and role in ROLE_KEYWORDS:
        role_keywords = ROLE_KEYWORDS[role]
        for category, keywords in role_keywords.items():
            for keyword in keywords:
                if keyword in job_desc and keyword not in resume_txt:
                    if keyword not in missing:
                        missing.append(keyword)
    
    return missing[:20]  # Return top 20 missing keywords

# ------------------------------
# Get role-specific recommendations
# ------------------------------
def get_role_recommendations(job):
    """Get recommendations based on detected role"""
    role = detect_role(job.job_description.lower())
    
    if not role or role not in ROLE_KEYWORDS:
        return None
    
    recommendations = {
        'role': role.replace('_', ' ').title(),
        'categories': {}
    }
    
    for category, keywords in ROLE_KEYWORDS[role].items():
        recommendations['categories'][category.title()] = keywords
    
    return recommendations
