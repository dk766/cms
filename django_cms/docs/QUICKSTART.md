# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd django_cms
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Database

For quick start, use SQLite (already configured):

```bash
cp .env.example .env
```

### Step 3: Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 4: Run Server

```bash
python manage.py runserver
```

### Step 5: Access Admin

1. Visit http://localhost:8000/admin/
2. Login with your superuser credentials
3. Start creating pages!

## 📝 Creating Your First Page

### 1. Configure Site Settings

1. Go to **Site Configuration**
2. Set your site name
3. Choose colors (optional)
4. Save

### 2. Create Homepage

1. Go to **Pages** → **Add Page**
2. Fill in:
   - **Title**: "Home"
   - **Status**: Published
   - **Is Home**: ✓ (check this)

3. **Add a Hero Section**:
   - Click "Add another Section"
   - Section Type: "Hero Section"
   - Title: "Welcome to Our Website"

4. **Add Content Blocks to Hero**:
   - **Block 1** (Heading):
     - Type: "Rich Text"
     - Content: "<h1>Welcome to Our Site</h1>"

   - **Block 2** (Button):
     - Type: "Button/CTA"
     - Link Text: "Learn More"
     - Link URL: "#about"
     - Button Style: "Primary"

5. **Add About Section**:
   - Section Type: "Text Section"
   - Anchor ID: "about"
   - Add Rich Text block with your content

6. **Save** and visit http://localhost:8000/

## 🎨 Styling Tips

### Colors
- Go to **Site Configuration**
- Set Primary Color (e.g., `#007bff`)
- Set Secondary Color (e.g., `#6c757d`)

### Section Backgrounds
- Edit any section
- Set Background Color or upload Background Image
- Adjust padding for spacing

### Navigation Menu
1. Go to **Menu Items**
2. Create menu items linking to:
   - Pages (select a page)
   - Sections (select page + section)
   - External URLs

## 📱 Section Examples

### Hero Banner
```
Section Type: Hero Section
Blocks:
  1. Rich Text: <h1>Your Headline</h1><p>Subheading text</p>
  2. Button: "Get Started" → #contact
```

### Feature Grid
```
Section Type: Features Grid
Blocks:
  1. Icon+Text: Feature 1 description
  2. Icon+Text: Feature 2 description
  3. Icon+Text: Feature 3 description
```

### Image Gallery
```
Section Type: Gallery
Blocks:
  1. Gallery: Upload multiple images
```

### FAQ
```
Section Type: FAQ
Blocks:
  1. Rich Text: Q: Question 1? A: Answer 1
  2. Rich Text: Q: Question 2? A: Answer 2
```

## 🔗 Creating Navigation

1. **Menu Items** → **Add Menu Item**
2. Link to Pages:
   - Label: "About"
   - Link Type: "Internal Page"
   - Page: Select "About" page

3. Link to Sections:
   - Label: "Contact"
   - Link Type: "Page Section"
   - Section: Select contact section

4. Dropdown Menus:
   - Create parent item: "Services"
   - Create child items with parent set to "Services"

## 📦 Next Steps

1. **Upload Logo**: Site Configuration → Logo
2. **Add Pages**: Create About, Services, Contact pages
3. **Customize Footer**: Site Configuration → Footer Text
4. **Add Social Links**: Site Configuration → Social Media URLs
5. **Configure SEO**: Each page has Meta Description field

## 🆘 Common Issues

### Static files not loading?
```bash
python manage.py collectstatic
```

### Changes not showing?
- Clear browser cache (Ctrl+Shift+R)
- Restart development server

### Images not uploading?
- Check media folder permissions
- Ensure Pillow is installed

## 📚 Learn More

- Read full README.md
- Check API documentation
- Review example templates
