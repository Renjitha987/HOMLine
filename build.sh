#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files into STATIC_ROOT
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Ensure initial services, categories, FAQs are populated
python manage.py seed_data || true

# Optionally create superuser if environment variables are present
if [[ -n "$DJANGO_SUPERUSER_USERNAME" && -n "$DJANGO_SUPERUSER_PASSWORD" ]]; then
  python manage.py createsuperuser --noinput || true
fi
