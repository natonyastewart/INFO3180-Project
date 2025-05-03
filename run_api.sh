#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export FLASK_APP=app/app.py
export FLASK_ENV=development

# Run Flask
flask run
