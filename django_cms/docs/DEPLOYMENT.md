# Production Deployment Guide

## 🚀 Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- Domain name configured
- SSL certificate (Let's Encrypt recommended)

#### Steps

1. **Clone repository on server**:
```bash
git clone <repository-url>
cd django_cms
```

2. **Configure environment**:
```bash
cp .env.example .env
nano .env
```

Update for production:
```env
SECRET_KEY=<generate-strong-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=cms_production
DB_USER=cms_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432
```

3. **Build and start services**:
```bash
docker-compose up -d --build
```

4. **Run migrations**:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

5. **Configure SSL with Certbot**:
```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Manual Deployment on Ubuntu Server

#### 1. Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install Python and dependencies
sudo apt-get install python3.11 python3.11-venv python3-pip
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install nginx
```

#### 2. PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE cms_production;
CREATE USER cms_user WITH PASSWORD 'strong_password';
ALTER ROLE cms_user SET client_encoding TO 'utf8';
ALTER ROLE cms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cms_production TO cms_user;
\q
```

#### 3. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/cms
sudo chown $USER:$USER /var/www/cms
cd /var/www/cms

# Clone repository
git clone <repository-url> .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp .env.example .env
nano .env
```

#### 4. Django Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create media directories
mkdir -p media/uploads media/thumbnails
```

#### 5. Gunicorn Configuration

Create systemd service file:

```bash
sudo nano /etc/systemd/system/cms.service
```

```ini
[Unit]
Description=Django CMS Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/cms
Environment="PATH=/var/www/cms/venv/bin"
EnvironmentFile=/var/www/cms/.env
ExecStart=/var/www/cms/venv/bin/gunicorn \
          --workers 4 \
          --bind unix:/var/www/cms/cms.sock \
          --access-logfile /var/log/cms/access.log \
          --error-logfile /var/log/cms/error.log \
          cms_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/cms
sudo chown www-data:www-data /var/log/cms

# Set permissions
sudo chown -R www-data:www-data /var/www/cms

# Enable and start service
sudo systemctl enable cms
sudo systemctl start cms
sudo systemctl status cms
```

#### 6. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/cms
```

```nginx
upstream cms_app {
    server unix:/var/www/cms/cms.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 100M;

    access_log /var/log/nginx/cms_access.log;
    error_log /var/log/nginx/cms_error.log;

    location /static/ {
        alias /var/www/cms/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/cms/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://cms_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

### Option 3: Platform-as-a-Service (PaaS)

#### Heroku

1. **Install Heroku CLI**
2. **Create app**:
```bash
heroku create your-cms-app
```

3. **Add PostgreSQL**:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Configure environment**:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-cms-app.herokuapp.com
```

5. **Deploy**:
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### DigitalOcean App Platform

1. Connect GitHub repository
2. Configure build settings
3. Add PostgreSQL database
4. Set environment variables
5. Deploy

## 📊 Monitoring & Maintenance

### Health Checks

Create a health check endpoint:

```python
# In cms_app/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "healthy"})
    except Exception as e:
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)
```

### Logging

Configure in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/cms/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Backups

#### Database Backup Script

```bash
#!/bin/bash
# /var/www/cms/backup.sh

BACKUP_DIR="/var/backups/cms"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -U cms_user cms_production > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/cms/media/

# Remove backups older than 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /var/www/cms/backup.sh
```

### Performance Tuning

#### 1. Redis Cache

```bash
pip install django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

#### 2. Database Connection Pooling

```bash
pip install psycopg2-pool
```

#### 3. CDN for Static Files

Use AWS S3 + CloudFront:

```bash
pip install django-storages boto3
```

```python
# settings.py
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = 'your-key'
    AWS_SECRET_ACCESS_KEY = 'your-secret'
    AWS_STORAGE_BUCKET_NAME = 'your-bucket'
```

## 🔒 Security Hardening

### 1. Security Headers

```python
# settings.py
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
```

### 2. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. Fail2ban

```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
```

### 4. Regular Updates

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade

# Update Python packages
pip install --upgrade -r requirements.txt
```

## 📈 Scaling

### Horizontal Scaling

1. **Load Balancer**: Use Nginx or AWS ELB
2. **Multiple App Servers**: Run multiple Gunicorn instances
3. **Shared Database**: Central PostgreSQL server
4. **Shared Media Storage**: S3 or shared NFS

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database (indexes, query optimization)
- Enable caching (Redis, Memcached)

## 🆘 Troubleshooting

### Service won't start
```bash
sudo systemctl status cms
sudo journalctl -u cms -n 50
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart cms
```

### Database connection errors
- Check PostgreSQL is running
- Verify credentials in .env
- Check firewall rules

### 502 Bad Gateway
- Check Gunicorn service is running
- Verify socket file permissions
- Check Nginx configuration

## 📞 Support

For deployment issues:
- Check logs: `/var/log/cms/`
- Nginx logs: `/var/log/nginx/`
- System logs: `sudo journalctl -xe`
