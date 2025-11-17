# Getting Started with Django CMS

Welcome! This guide will help you get the Django CMS up and running in minutes.

## 🚀 Quick Start (3 Steps)

### Step 1: Run Setup Script

The easiest way to get started is using our automated setup script:

```bash
cd /home/user/cms/django_cms
./scripts/setup.sh
```

This script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Generate secure SECRET_KEY
- ✅ Create .env file
- ✅ Create media directories
- ✅ Run database migrations
- ✅ Collect static files
- ✅ Create superuser account

### Step 2: Load Demo Content (Optional)

Want to see the CMS in action immediately? Load demo data:

```bash
source venv/bin/activate
python manage.py create_demo_site
```

This creates:
- 📄 Homepage with hero section and features
- 📄 About page
- 📄 Services page
- 📄 Contact page
- 🔗 Navigation menu
- ⚙️ Site configuration

### Step 3: Start the Server

```bash
python manage.py runserver
```

**Access your site:**
- 🌐 Frontend: http://localhost:8000/
- 👨‍💼 Admin: http://localhost:8000/admin/
- 🔌 API: http://localhost:8000/api/

**Demo credentials** (if you used create_demo_site):
- Username: `admin`
- Password: `admin`

---

## 📖 Manual Setup

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set your SECRET_KEY:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Generate a secure key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Database Setup

Run migrations:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Start Development Server

```bash
python manage.py runserver
```

---

## 🎨 Creating Your First Page

### Via Admin Interface

1. **Login** to admin at http://localhost:8000/admin/

2. **Go to Pages** → **Add Page**

3. **Fill in basic info**:
   - Title: "My First Page"
   - Slug: "my-first-page" (auto-generated)
   - Status: "Published"

4. **Add a Section** (scroll down to "Sections"):
   - Click "Add another Section"
   - Section Type: "Hero Section"
   - Title: "Welcome Section"

5. **Add Content Blocks** to the section:
   - Click "Add another Content Block"
   - Block Type: "Rich Text"
   - Content: Enter your text

6. **Save** and visit http://localhost:8000/my-first-page/

### Programmatically

```python
from cms_app.models import Page, Section, ContentBlock

# Create page
page = Page.objects.create(
    title="My Page",
    status="published"
)

# Add section
section = Section.objects.create(
    page=page,
    section_type="hero",
    title="Welcome"
)

# Add content
ContentBlock.objects.create(
    section=section,
    block_type="rich_text",
    content="<h1>Hello World!</h1>"
)
```

---

## 🎯 Common Tasks

### Adding Navigation Menu

1. **Admin** → **Menu Items** → **Add Menu Item**
2. Set:
   - Label: "Home"
   - Link Type: "Internal Page"
   - Page: Select your page
   - Order: 0

### Customizing Site Appearance

1. **Admin** → **Site Configuration**
2. Customize:
   - Site Name
   - Colors (Primary, Secondary)
   - Logo/Favicon
   - Footer Text

### Uploading Media

1. **Admin** → **Media Files** → **Add Media File**
2. Upload file and add metadata
3. Use in content blocks

### Creating a Gallery

1. Create a section with type "Gallery"
2. Add a content block with type "Gallery"
3. Add gallery images (inline)

---

## 🔌 Using the API

### Get All Pages

```bash
curl http://localhost:8000/api/pages/
```

### Get Homepage

```bash
curl http://localhost:8000/api/pages/homepage/
```

### Get Site Configuration

```bash
curl http://localhost:8000/api/site-config/current/
```

### JavaScript Example

```javascript
fetch('http://localhost:8000/api/pages/homepage/')
  .then(res => res.json())
  .then(data => {
    console.log(data);
    // data.sections contains all sections
    // each section has content_blocks
  });
```

---

## 🐳 Docker Setup

### Using Docker Compose

```bash
# Build and start
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f
```

Access at http://localhost/

---

## 📚 Next Steps

### Learn More
- 📖 Read the [Full Documentation](README.md)
- 🏗️ Understand the [Architecture](docs/ARCHITECTURE.md)
- 🚀 Learn about [Deployment](docs/DEPLOYMENT.md)
- 🔌 Explore the [API](docs/API_DOCUMENTATION.md)

### Customize
- **Templates**: Edit files in `cms_app/templates/`
- **Styles**: Modify `cms_app/static/css/custom.css`
- **JavaScript**: Update `cms_app/static/js/custom.js`
- **Models**: Extend models in `cms_app/models.py`

### Build Your Site
1. Create pages for your content
2. Design sections with different types
3. Add content blocks
4. Customize navigation
5. Upload media files
6. Configure site settings

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8080
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Permission Errors (Media)
```bash
chmod -R 755 media/
```

---

## 💡 Tips

1. **Use the demo site** - Load demo data to see examples
2. **Start simple** - Begin with basic pages, add complexity later
3. **Preview often** - Use preview links in admin
4. **Check the API** - API responses show data structure
5. **Read docs** - Comprehensive guides in `/docs/` folder

---

## 🎓 Example Workflows

### Creating a Marketing Site

1. **Homepage**: Hero section + Features + CTA
2. **About Page**: Two-column layout with story
3. **Services**: Three-column features grid
4. **Testimonials**: Testimonials section
5. **Contact**: Contact form section

### Creating a Blog-Style Site

1. Create page for each article
2. Use rich text blocks for content
3. Add images and galleries
4. Use navigation for categories
5. Leverage SEO features

### Creating a Portfolio

1. Gallery sections for projects
2. Two-column layouts for details
3. Image blocks for showcasing work
4. Contact section for inquiries

---

## ✅ Checklist

Before going live:

- [ ] Configure site settings
- [ ] Upload logo and favicon
- [ ] Set primary/secondary colors
- [ ] Create all pages
- [ ] Build navigation menu
- [ ] Add SEO meta descriptions
- [ ] Upload media files
- [ ] Test on mobile devices
- [ ] Check all links
- [ ] Review content
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up SSL certificate

---

## 🤝 Getting Help

- **Documentation**: Check `/docs/` folder
- **Admin Interface**: Explore inline help text
- **API Browser**: Visit http://localhost:8000/api/
- **Code Comments**: Read inline comments in code

---

**Ready to build something amazing? Let's go! 🚀**
