# Django CMS - Production-Ready Content Management System

A powerful, flexible Django-based CMS for creating marketing websites with a beautiful admin interface and Bootstrap 5 frontend.

## 🚀 Features

- **User-Friendly Admin Interface**: Intuitive Django admin with inline editors, drag-and-drop sorting, and rich text editing
- **Flexible Page Builder**: Create pages with multiple sections and content blocks
- **12+ Section Types**: Hero, text, gallery, carousel, FAQ, CTA, testimonials, features, and more
- **10+ Content Block Types**: Rich text, images, galleries, videos, buttons, icons, code blocks
- **Navigation System**: Fully customizable menus with dropdown support and section anchors
- **Media Library**: Organized media management with thumbnails and metadata
- **Theming**: Site-wide color schemes, typography, and branding
- **SEO Optimized**: Meta tags, OpenGraph, sitemap.xml, robots.txt
- **REST API**: Full-featured API for headless CMS usage
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Performance**: Template caching, lazy loading, optimized queries

## 📋 Requirements

- Python 3.10+
- PostgreSQL 12+ (or SQLite for development)
- pip and virtualenv

## 🛠️ Installation

### 1. Clone the Repository

```bash
cd django_cms
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and update the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cms_db
DB_USER=cms_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# For SQLite (development)
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Frontend**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

## 📁 Project Structure

```
django_cms/
├── cms_project/              # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
├── cms_app/                  # Main CMS application
│   ├── models.py            # Database models
│   ├── admin.py             # Admin configuration
│   ├── views.py             # Views
│   ├── urls.py              # URL patterns
│   ├── signals.py           # Signal handlers
│   ├── context_processors.py
│   ├── api/                 # REST API
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── templatetags/        # Custom template tags
│   │   └── cms_tags.py
│   ├── templates/           # HTML templates
│   │   └── cms_app/
│   │       ├── base.html
│   │       ├── page.html
│   │       └── includes/
│   └── static/              # Static files
│       ├── css/
│       └── js/
├── media/                    # User uploads
├── static/                   # Collected static files
├── requirements.txt
├── manage.py
└── README.md
```

## 🎨 Usage Guide

### Creating Your First Page

1. **Login to Admin** at http://localhost:8000/admin/
2. **Navigate to Pages** → Add Page
3. **Fill in page details**:
   - Title: "Home"
   - Slug: "home" (auto-generated)
   - Status: Published
   - Is Home: ✓ (check this for homepage)

4. **Add Sections** (inline editor):
   - Click "Add another Section"
   - Choose section type (e.g., "Hero Section")
   - Set title, anchor ID, styling options

5. **Add Content Blocks** to each section:
   - Click "Add another Content Block"
   - Choose block type (e.g., "Rich Text", "Image", "Button")
   - Fill in content

6. **Save** and visit your homepage!

### Section Types

- **Hero**: Large banner with title, text, and CTA
- **Text**: Simple text content
- **Two/Three Column**: Multi-column layouts
- **Gallery**: Image grid
- **Carousel**: Image/content slider
- **Features**: Icon + text grid
- **FAQ**: Accordion-style questions
- **CTA**: Call-to-action section
- **Testimonials**: Customer reviews
- **Contact**: Contact information

### Content Block Types

- **Rich Text**: WYSIWYG editor for formatted text
- **Heading**: Customizable headings (H1-H6)
- **Image**: Single image with caption
- **Gallery**: Multiple images
- **Video**: YouTube/Vimeo embeds
- **Button**: Call-to-action buttons
- **Icon + Text**: Feature cards
- **Code**: Syntax-highlighted code blocks
- **Spacer**: Vertical spacing
- **Divider**: Horizontal line
- **HTML**: Raw HTML content

### Creating Navigation Menus

1. **Go to Menu Items** in admin
2. **Add menu item**:
   - Label: "About Us"
   - Link Type: "Internal Page" or "Page Section"
   - Select target page/section
3. **Set order** for menu position
4. **Create dropdowns** by setting a parent menu item

### Configuring Site Settings

1. **Go to Site Configuration**
2. **Customize**:
   - Site name, logo, favicon
   - Primary/secondary colors
   - Typography settings
   - Footer content
   - Social media links
   - SEO defaults

### Using the Media Library

1. **Go to Media Files** in admin
2. **Upload files** with metadata:
   - Title, alt text, caption
   - Tags for organization
3. **Browse media** at http://localhost:8000/media-library/

## 🔌 REST API

The CMS includes a full REST API for headless usage.

### API Endpoints

```
GET /api/pages/                    # List all published pages
GET /api/pages/{slug}/             # Get page with sections & blocks
GET /api/pages/homepage/           # Get homepage
GET /api/sections/                 # List sections
GET /api/sections/{id}/            # Get section with blocks
GET /api/content-blocks/           # List content blocks
GET /api/menu-items/               # Get navigation menu
GET /api/media/                    # List media files
GET /api/site-config/current/      # Get site configuration
```

### API Example

```bash
# Get homepage data
curl http://localhost:8000/api/pages/homepage/

# Get all pages
curl http://localhost:8000/api/pages/

# Get specific page
curl http://localhost:8000/api/pages/about/
```

## 🚀 Production Deployment

### Using Docker

1. **Build and run with Docker Compose**:

```bash
docker-compose up -d
```

2. **Run migrations inside container**:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### Manual Deployment

#### 1. Update Settings

In `settings.py` for production:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

#### 2. Use PostgreSQL

Set up PostgreSQL database and update `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cms_production
DB_USER=cms_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=5432
```

#### 3. Configure Static/Media Files

```bash
python manage.py collectstatic --noinput
```

#### 4. Set Up Gunicorn

```bash
gunicorn cms_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

#### 5. Configure Nginx

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/django_cms/staticfiles/;
    }

    location /media/ {
        alias /path/to/django_cms/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 6. Set Up SSL with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 7. Process Management

Use systemd or supervisor to manage Gunicorn:

```ini
# /etc/systemd/system/cms.service
[Unit]
Description=Django CMS
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/django_cms
ExecStart=/path/to/venv/bin/gunicorn cms_project.wsgi:application --bind 0.0.0.0:8000 --workers 4

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable cms
sudo systemctl start cms
```

## 🔒 Security Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set secure cookie flags
- [ ] Configure CSRF protection
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Limit admin access
- [ ] Enable database backups

## 🎯 Performance Optimization

1. **Enable caching**:
   - Template caching (already configured)
   - Redis/Memcached for production

2. **Optimize database**:
   - Use select_related/prefetch_related (already done)
   - Add database indexes if needed

3. **CDN for static files**:
   - Use AWS S3 or similar for media
   - CloudFront for static files

4. **Image optimization**:
   - Compress images before upload
   - Use WebP format
   - Lazy loading (already implemented)

## 🧪 Testing

Run tests:

```bash
python manage.py test
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Support

For issues and questions:
- Check the documentation
- Review example websites
- Contact support team

## 🎓 Example Website

This CMS can create sites like: https://info.arhivadefacturi.ro/

Features demonstrated:
- Clean navigation
- Hero sections
- Feature grids
- Call-to-action buttons
- Responsive design
- Professional styling
