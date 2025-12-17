#!/bin/bash
# Build script for Render deployment

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Clear any existing static files
rm -rf staticfiles

# Collect static files
python manage.py collectstatic --noinput --clear

# Run database migrations
python manage.py migrate --noinput

# List collected static files for debugging
echo "Static files collected:"
ls -la staticfiles/ || echo "No staticfiles directory found"



