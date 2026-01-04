#!/bin/bash

# Navigate to project directory
cd "/home/vanam-pranav/Downloads/WhatSie/resume pranav/ats_resume"

# Activate virtual environment
source venv/bin/activate

# Start server
echo "Starting development server..."
exec python manage.py runserver
