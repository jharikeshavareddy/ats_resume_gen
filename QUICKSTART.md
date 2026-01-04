# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Activate Virtual Environment
```bash
cd "/home/vanam-pranav/Downloads/WhatSie/resume pranav/ats_resume"
source venv/bin/activate
```

### Step 2: Run Setup Script
```bash
./setup.sh
```

This will:
- Install all dependencies
- Download spaCy language model
- Create database tables

### Step 3: Start the Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📝 What's New?

### Enhanced Features

1. **Complete Resume Sections**
   - Personal Information with social links
   - Objective/Career Summary
   - Education
   - Work Experience (with detailed descriptions)
   - Projects
   - Technical Skills
   - Certifications
   - Extra-Curricular Activities
   - Honours and Achievements

2. **Full Edit Functionality**
   - Edit all resume information
   - Add/Delete entries for each section
   - Real-time preview

3. **LaTeX Export**
   - Professional LaTeX template (based on your format)
   - Automatic formatting with proper spacing
   - BrickRed color scheme
   - FontAwesome icons

4. **PDF Export**
   - Direct PDF generation (requires pdflatex)
   - Fallback to LaTeX download if pdflatex not available

---

## 🎯 How to Use

### Creating Your First Resume

1. **Register** an account at http://127.0.0.1:8000/register/
2. **Login** and go to Dashboard
3. **Create Resume** - Fill in basic information
4. **Edit Resume** - Add all sections:
   - Click "Add Education" to add your degrees
   - Click "Add Experience" to add work history
   - Click "Add Project" to showcase your projects
   - Click "Add Certification" for certifications
   - Click "Add Activity" for volunteer work
   - Click "Add Achievement" for awards

### Editing Resume

From the **Edit Resume** page:
- Update basic info in the main form
- Use section-specific "Add" buttons
- Delete unwanted entries with trash icon
- Preview anytime with "Preview" button

### Exporting Resume

Three export options available:

1. **DOCX** - Microsoft Word format
2. **LaTeX** - `.tex` source file for customization
3. **PDF** - Ready-to-use PDF (requires pdflatex)

---

## 📋 Example Data Entry

### Work Experience
```
Company: The EleFit Store
Position: Full-Stack Developer Intern
Start Date: Jan 2025
End Date: Present
Location: Remote, United States
Description: (Enter each point on a new line)
Developed and deployed the EleFit App
Implemented responsive UI with dynamic product browsing
Optimized backend Shopify GraphQL queries
```

### Project
```
Title: EleFit App – Flutter E-commerce Platform
Description: (Enter each point on a new line)
Built a cross-platform e-commerce app using Flutter
Implemented in-app checkout with secure WebView
Managed product catalog and caching
```

### Certification
```
Name: Introduction to Cybersecurity
Organization: Cisco Networking Academy
Issue Date: 2024
```

---

## 🔧 Troubleshooting

### Virtual Environment Not Activated?
```bash
source venv/bin/activate
```

### Missing Dependencies?
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Database Issues?
```bash
python manage.py makemigrations
python manage.py migrate
```

### PDF Export Not Working?
Install LaTeX:
```bash
sudo apt-get install texlive-full
```

Or download the LaTeX file and compile locally.

---

## 📚 Full Documentation

See `README.md` for complete documentation.

---

## ✨ Features Summary

✅ **Full CRUD Operations** - Create, Read, Update, Delete all resume sections  
✅ **Professional LaTeX Template** - Based on your provided format  
✅ **Multiple Export Formats** - DOCX, LaTeX, PDF  
✅ **ATS Scoring** - Match resume against job descriptions  
✅ **Responsive UI** - Bootstrap-based modern interface  
✅ **User Authentication** - Secure login/registration  
✅ **Multiple Resumes** - Create and manage multiple versions  

---

**Ready to build your professional resume? Start the server and visit http://127.0.0.1:8000/**
