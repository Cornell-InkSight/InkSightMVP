#!/bin/bash
# Activate virtual environment (if it exists)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run Django migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the Gunicorn server
gunicorn InkSightMVP.wsgi:application --bind 0.0.0.0:8000