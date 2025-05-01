#!/usr/bin/env fish

# Activate virtual environment
source venv/bin/activate.fish

# Set environment variables
set -x FLASK_APP app/app.py
set -x FLASK_ENV development

# Run Flask
flask run
