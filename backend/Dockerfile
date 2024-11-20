# Use the official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000
EXPOSE 8080

# Run the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_fake_data && gunicorn InkSightMVP.wsgi --bind 0.0.0.0:8080"]