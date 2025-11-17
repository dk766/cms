# Cloning Websites into Django CMS

This guide explains how to clone existing websites into your Django CMS.

## 📋 Overview

The CMS includes two web scraping tools to clone websites:

1. **clone_arhiva_site** - Uses requests and BeautifulSoup (faster, simpler)
2. **clone_arhiva_selenium** - Uses Selenium WebDriver (better for protected sites)

Both scripts will:
- ✅ Scrape website content and structure
- ✅ Download all images
- ✅ Extract color schemes and styling
- ✅ Create pages, sections, and content blocks
- ✅ Set up navigation menus
- ✅ Configure site settings

## 🚀 Quick Start

### Method 1: Simple Scraper (Recommended First)

```bash
cd /home/user/cms/django_cms
source venv/bin/activate
python manage.py clone_arhiva_site
```

If you get a 403 error, use Method 2.

### Method 2: Selenium Scraper (For Protected Sites)

```bash
# Install additional requirements
pip install -r requirements_scraping.txt

# Run the scraper
python manage.py clone_arhiva_selenium
```

## 📦 Installation

### Install Scraping Dependencies

```bash
pip install -r requirements_scraping.txt
```

This installs:
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML parser
- `requests` - HTTP requests
- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management

### For Selenium Method

Selenium requires Chrome or Chromium browser:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver
```

**macOS:**
```bash
brew install chromium
```

**The script will auto-download ChromeDriver if needed.**

## 🎯 Usage

### Basic Usage

```bash
# Clone https://info.arhivadefacturi.ro/
python manage.py clone_arhiva_site
```

### Advanced Options

```bash
# Skip downloading images (faster)
python manage.py clone_arhiva_site --skip-images

# Selenium with headless mode (no browser window)
python manage.py clone_arhiva_selenium --headless

# Selenium with visible browser (for debugging)
python manage.py clone_arhiva_selenium

# Skip images with Selenium
python manage.py clone_arhiva_selenium --headless --skip-images
```

## 📖 How It Works

### 1. Fetch Website

The script loads the target website and parses the HTML.

**Simple Scraper:**
- Uses `requests` library
- Fast and lightweight
- May be blocked by anti-bot protection

**Selenium Scraper:**
- Uses real Chrome browser
- Executes JavaScript
- Bypasses most bot protection
- Slower but more reliable

### 2. Extract Structure

The script identifies:
- **Sections** - Main content areas (hero, features, contact, etc.)
- **Content Blocks** - Text, images, buttons within sections
- **Navigation** - Menu items and links
- **Colors** - Primary, secondary, background colors
- **Branding** - Logo, favicon, site name

### 3. Download Media

All images are downloaded and saved to the Media library:
- Images are saved with original filenames
- Alt text and captions are preserved
- Background images are identified

### 4. Create CMS Objects

The script creates:
- **Site Configuration** - Colors, branding, footer
- **Homepage** - With all sections and content
- **Menu Items** - Navigation structure

## 🎨 Section Detection

The scraper automatically detects section types:

| HTML Pattern | CMS Section Type |
|--------------|------------------|
| `class="hero"` or `class="banner"` | Hero Section |
| `class="features"` or `class="services"` | Features Grid |
| `class="gallery"` or `class="portfolio"` | Gallery |
| `class="testimonial"` | Testimonials |
| `class="contact"` | Contact Section |
| `class="faq"` | FAQ Accordion |
| `class="cta"` or `class="call-to-action"` | Call to Action |
| First section | Hero (default) |
| Other sections | Text Section |

## 🖼️ Content Block Detection

The scraper extracts:

| Element | CMS Block Type |
|---------|----------------|
| `<p>`, `<h1-6>`, `<div>` text | Rich Text |
| `<img>` tags | Image |
| `<a class="btn">` | Button/CTA |
| Multiple `<img>` in section | Gallery |

## ⚙️ Customizing the Scraper

### Clone a Different Website

Edit the script to change the target URL:

```python
# In cms_app/management/commands/clone_arhiva_site.py
self.base_url = 'https://your-target-site.com'
```

### Adjust Section Detection

Modify the `create_section_from_element` method to detect your site's structure:

```python
def create_section_from_element(self, page, element, order):
    # Add custom detection logic
    if 'your-custom-class' in class_str:
        section_type = 'custom'
```

### Custom Content Extraction

Edit `parse_content_blocks` to extract specific content:

```python
def parse_content_blocks(self, element, section):
    # Add custom extraction logic
    custom_elements = element.find_all('div', class_='your-class')
    for elem in custom_elements:
        # Create content blocks
        pass
```

## 🔧 Troubleshooting

### 403 Forbidden Error

**Problem:** Website blocks automated requests.

**Solutions:**
1. Use Selenium scraper: `python manage.py clone_arhiva_selenium`
2. Add delays between requests
3. Use VPN or proxy

### No Sections Created

**Problem:** Script couldn't identify sections.

**Check:**
- Website HTML structure
- Look for `<section>` tags or `div` with classes
- Adjust section detection logic

### Images Not Downloading

**Problem:** Image URLs are relative or protected.

**Solutions:**
1. Run with `--skip-images` first to test structure
2. Check image URLs in browser
3. Manually upload images to Media library

### Selenium Issues

**Problem:** ChromeDriver not found or version mismatch.

**Solution:**
```bash
# Reinstall webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager

# Or install ChromeDriver manually
# Ubuntu:
sudo apt-get install chromium-chromedriver

# macOS:
brew install chromedriver
```

### Memory Issues

**Problem:** Large websites cause memory errors.

**Solutions:**
- Limit sections: Modify script to only scrape first 5 sections
- Skip images: Use `--skip-images`
- Increase system memory

## 📝 Manual Review

After cloning, review and adjust:

1. **Visit Site**: http://localhost:8000/
2. **Check Admin**: http://localhost:8000/admin/
3. **Adjust Content**:
   - Edit section titles
   - Reorder sections
   - Fix broken images
   - Update colors in Site Configuration
   - Adjust navigation menu

## 🎯 Best Practices

### Before Cloning

1. **Check robots.txt**: Ensure scraping is allowed
2. **Review Terms of Service**: Get permission if needed
3. **Backup Database**: `python manage.py dumpdata > backup.json`

### After Cloning

1. **Review Content**: Check all sections render correctly
2. **Fix Links**: Update internal links to point to your CMS
3. **Optimize Images**: Compress large images
4. **Test Responsive**: Check mobile view
5. **SEO**: Update meta descriptions

### Legal Considerations

- ⚠️ **Only clone websites you own or have permission to clone**
- ⚠️ **Respect copyright and intellectual property**
- ⚠️ **Check the website's robots.txt and terms of service**
- ⚠️ **Don't overload servers with too many requests**
- ⚠️ **Use for learning and development purposes**

## 🔄 Re-running the Script

If you run the script again:
- Existing homepage sections will be **deleted**
- New content will be created
- Site configuration will be **updated**
- Menu items will be **replaced**

To preserve content:
- Backup first: `python manage.py dumpdata > backup.json`
- Or create a new page instead of replacing homepage

## 📊 Performance

### Simple Scraper (requests)
- Speed: ⚡⚡⚡ Fast (2-10 seconds)
- Success Rate: 60% (blocked by anti-bot)
- Resource Usage: Low

### Selenium Scraper
- Speed: ⚡⚡ Medium (10-30 seconds)
- Success Rate: 95% (bypasses most protection)
- Resource Usage: High (requires Chrome)

## 🎓 Examples

### Clone and Preview

```bash
# Full clone
python manage.py clone_arhiva_selenium --headless

# Start server
python manage.py runserver

# Open browser to http://localhost:8000/
```

### Clone Without Images

```bash
# Fast structure clone
python manage.py clone_arhiva_site --skip-images

# Review structure
# Then download images manually
```

### Debug Mode

```bash
# See browser window
python manage.py clone_arhiva_selenium

# Watch the scraping process
# Useful for debugging
```

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**: Script outputs detailed progress
2. **Verify Source**: Visit target website in browser
3. **Test Manually**: Try downloading an image URL manually
4. **Adjust Script**: Customize for your target site
5. **Ask for Help**: Include error messages and target URL

## 🚀 Next Steps

After cloning:

1. **Customize Content**: Edit in admin
2. **Add Pages**: Create additional pages
3. **Adjust Styling**: Update colors and fonts
4. **Optimize SEO**: Add meta descriptions
5. **Deploy**: Follow deployment guide

---

**Happy Cloning! 🎉**
