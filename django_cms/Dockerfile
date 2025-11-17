# Dockerfile for Django CMS

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create directories for media
RUN mkdir -p /app/media/uploads /app/media/thumbnails

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "cms_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
