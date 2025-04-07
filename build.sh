#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

mkdir -p staticfiles
mkdir -p static
mkdir -p media/found_items
mkdir -p media/lost_items

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

chmod +x build.sh