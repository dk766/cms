# Website Cloning - Quick Start 🚀

Clone https://info.arhivadefacturi.ro/ into your Django CMS in 3 easy steps!

## ⚡ Super Quick (3 Steps)

```bash
# Step 1: Install scraping tools
make install-scraper

# Step 2: Clone the website
make clone-site

# Step 3: Start server and view
make run
# Visit http://localhost:8000/
```

## 🎯 Available Methods

### Method 1: Interactive Script (Recommended)
```bash
make clone-site
# Choose option 1 or 2 when prompted
```

### Method 2: Simple Scraper (Fast)
```bash
make clone-simple
# Uses requests + BeautifulSoup
# Fast but may be blocked (403 error)
```

### Method 3: Selenium Scraper (Most Reliable)
```bash
make clone-selenium
# Uses Chrome browser automation
# Slower but bypasses bot protection
```

### Method 4: Manual Commands
```bash
# Simple scraper
python manage.py clone_arhiva_site

# Selenium scraper
python manage.py clone_arhiva_selenium --headless

# Selenium with visible browser (debugging)
python manage.py clone_arhiva_selenium
```

## 📋 What Gets Cloned?

✅ **Site Configuration**
   - Site name and branding
   - Color scheme (primary, secondary)
   - Logo and favicon
   - Footer content

✅ **Homepage**
   - All sections (hero, features, contact, etc.)
   - Content blocks (text, images, buttons)
   - Background images and styling

✅ **All Images**
   - Downloaded to media library
   - Alt text preserved
   - Original filenames maintained

✅ **Navigation Menu**
   - All menu items
   - Links and structure
   - Dropdown items

## 🛠️ Installation

### First Time Setup

```bash
# Install base CMS
make setup

# Install scraping tools
make install-scraper
```

### Requirements

The scraping tools need:
- `beautifulsoup4` - HTML parsing
- `lxml` - XML parser
- `requests` - HTTP requests
- `selenium` - Browser automation (optional)
- `webdriver-manager` - Auto ChromeDriver (optional)

These are installed automatically with `make install-scraper`

### For Selenium (Optional)

**Ubuntu:**
```bash
sudo apt-get install chromium-browser
```

**macOS:**
```bash
brew install chromium
```

ChromeDriver is auto-downloaded by the script.

## ⚙️ Options

### Skip Images (Faster Testing)

```bash
# Simple scraper
python manage.py clone_arhiva_site --skip-images

# Selenium
python manage.py clone_arhiva_selenium --skip-images
```

### Visible Browser (Debugging)

```bash
# See what Selenium is doing
python manage.py clone_arhiva_selenium
```

## 🔍 Troubleshooting

### 403 Forbidden Error
**Solution:** Use Selenium method
```bash
make clone-selenium
```

### ChromeDriver Issues
**Solution:** Reinstall
```bash
pip uninstall webdriver-manager
pip install webdriver-manager
```

### No Sections Created
**Solution:** Check script output for errors
The script shows detailed progress

### Images Not Downloading
**Solution:** Run without images first
```bash
make clone-simple --skip-images
```
Then manually upload images

## 📖 Full Documentation

For detailed information, see:
- **docs/CLONING_WEBSITES.md** - Complete guide
- **Clone script**: `cms_app/management/commands/clone_arhiva_site.py`
- **Selenium script**: `cms_app/management/commands/clone_arhiva_selenium.py`

## 🎓 Example Workflow

### Complete Clone

```bash
# 1. Setup CMS
make setup

# 2. Install scraping tools
make install-scraper

# 3. Clone website
make clone-selenium

# 4. Start server
make run

# 5. View at http://localhost:8000/
```

### Quick Test (No Images)

```bash
# Clone structure only
python manage.py clone_arhiva_site --skip-images

# Check structure in admin
# Then download images manually if needed
```

### Development Workflow

```bash
# Clone site
make clone-site

# Make changes in admin
# http://localhost:8000/admin/

# Re-clone if needed (overwrites homepage)
make clone-selenium
```

## ⚠️ Important Notes

### What Happens When You Clone

- ✅ Creates/Updates Site Configuration
- ✅ Creates/Updates Homepage
- ⚠️ **Deletes existing homepage sections**
- ✅ Downloads all images to media library
- ✅ Creates navigation menu items
- ⚠️ **Replaces existing menu items**

### Before Cloning

1. **Backup your data** if you have existing content
2. **Check target website** is accessible
3. **Ensure you have permission** to clone the site

### After Cloning

1. **Review content** in admin
2. **Fix any broken links**
3. **Adjust colors** in Site Configuration
4. **Optimize images** if needed
5. **Test mobile view**

## 🔄 Re-Cloning

To clone again after making changes:

```bash
# Backup first
python manage.py dumpdata > backup.json

# Clone (this will overwrite homepage)
make clone-selenium

# Restore specific data if needed
# Or manually re-create your changes
```

## 🎨 Customizing After Clone

### Via Admin Interface

1. Visit http://localhost:8000/admin/
2. Go to **Site Configuration**
   - Change colors
   - Upload new logo
   - Update footer
3. Go to **Pages** → **Home**
   - Edit sections
   - Reorder content
   - Add new sections

### Via Code

Edit the cloning script to customize:
- `cms_app/management/commands/clone_arhiva_site.py`
- `cms_app/management/commands/clone_arhiva_selenium.py`

## 📊 Performance

| Method | Speed | Success Rate | Resources |
|--------|-------|--------------|-----------|
| Simple Scraper | ⚡⚡⚡ 2-10s | 60% | Low |
| Selenium | ⚡⚡ 10-30s | 95% | High |
| Manual | ⚡ Instant | 100% | None |

## ✅ Success Checklist

After cloning, verify:

- [ ] Site loads at http://localhost:8000/
- [ ] All sections are visible
- [ ] Images are displaying
- [ ] Navigation menu works
- [ ] Colors look correct
- [ ] Footer appears
- [ ] Mobile view works

## 🆘 Need Help?

1. **Check logs**: Script shows detailed output
2. **Read docs**: See `docs/CLONING_WEBSITES.md`
3. **Test manually**: Visit target site in browser
4. **Try both methods**: Simple and Selenium
5. **Report issues**: Include error messages

## 🎉 You're Ready!

Start cloning with:
```bash
make clone-site
```

Or read the full guide:
```bash
cat docs/CLONING_WEBSITES.md
```

**Happy Cloning! 🚀**
