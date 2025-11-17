"""
Enhanced Django management command to clone https://info.arhivadefacturi.ro/
Uses Selenium to bypass bot protection.

Usage: python manage.py clone_arhiva_selenium
"""
import os
import re
import time
from urllib.parse import urljoin, urlparse
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

import requests
from cms_app.models import (
    SiteConfiguration, Page, Section, ContentBlock, MenuItem, Media
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Clones https://info.arhivadefacturi.ro/ using Selenium'

    def __init__(self):
        super().__init__()
        self.base_url = 'https://info.arhivadefacturi.ro'
        self.driver = None
        self.downloaded_images = {}
        self.user = None
        self.session = requests.Session()

    def add_arguments(self, parser):
        parser.add_argument(
            '--headless',
            action='store_true',
            help='Run browser in headless mode',
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Skip downloading images',
        )

    def handle(self, *args, **options):
        if not SELENIUM_AVAILABLE:
            self.stdout.write(self.style.ERROR(
                'Selenium not installed. Install with: pip install -r requirements_scraping.txt'
            ))
            return

        self.headless = options.get('headless', True)
        self.skip_images = options.get('skip_images', False)

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('  Cloning https://info.arhivadefacturi.ro/'))
        self.stdout.write(self.style.SUCCESS('  Using Selenium WebDriver'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Get or create admin user
        self.user = User.objects.filter(is_superuser=True).first()
        if not self.user:
            self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
            return

        try:
            # Initialize Selenium
            self.stdout.write('Initializing browser...')
            self.init_selenium()

            # Step 1: Fetch homepage
            self.stdout.write('Step 1: Loading homepage...')
            self.driver.get(self.base_url)
            time.sleep(3)  # Wait for page to load

            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Step 2: Extract site configuration
            self.stdout.write('Step 2: Extracting site configuration...')
            self.setup_site_config(soup)

            # Step 3: Clone homepage
            self.stdout.write('Step 3: Cloning homepage...')
            self.clone_homepage(soup)

            # Step 4: Setup navigation
            self.stdout.write('Step 4: Setting up navigation...')
            self.setup_navigation(soup)

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write(self.style.SUCCESS('  Site cloned successfully!'))
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write('')
            self.stdout.write('Visit http://localhost:8000/ to see the cloned site')
            self.stdout.write('')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()

        finally:
            if self.driver:
                self.driver.quit()

    def init_selenium(self):
        """Initialize Selenium WebDriver."""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(30)

    def download_image(self, img_url):
        """Download an image and save it to Media library."""
        if img_url in self.downloaded_images:
            return self.downloaded_images[img_url]

        if self.skip_images:
            return None

        try:
            # Make URL absolute
            if not img_url.startswith('http'):
                img_url = urljoin(self.base_url, img_url)

            # Skip data URLs
            if img_url.startswith('data:'):
                return None

            # Download image using Selenium's session cookies
            response = self.session.get(img_url, timeout=30)
            response.raise_for_status()

            # Get filename
            filename = os.path.basename(urlparse(img_url).path)
            if not filename or '.' not in filename:
                filename = f'image_{len(self.downloaded_images)}.jpg'

            # Create Media object
            media = Media.objects.create(
                title=filename,
                uploaded_by=self.user
            )
            media.file.save(filename, ContentFile(response.content), save=True)

            self.downloaded_images[img_url] = media
            self.stdout.write(self.style.SUCCESS(f'  ✓ Downloaded: {filename}'))
            return media

        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ✗ Failed to download {img_url}: {str(e)}'))
            return None

    def extract_colors(self, soup):
        """Extract color scheme from the page."""
        colors = {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'background': '#ffffff',
            'text': '#212529'
        }

        # Try to extract from computed styles using Selenium
        try:
            # Get primary color from elements
            elements = self.driver.find_elements(By.CSS_SELECTOR, '.btn-primary, .bg-primary, [class*="primary"]')
            if elements:
                bg_color = elements[0].value_of_css_property('background-color')
                if bg_color:
                    colors['primary'] = self.rgb_to_hex(bg_color)
        except:
            pass

        return colors

    def rgb_to_hex(self, rgb_string):
        """Convert RGB color to hex."""
        try:
            if rgb_string.startswith('#'):
                return rgb_string

            # Extract numbers from "rgb(r, g, b)" or "rgba(r, g, b, a)"
            numbers = re.findall(r'\d+', rgb_string)
            if len(numbers) >= 3:
                r, g, b = int(numbers[0]), int(numbers[1]), int(numbers[2])
                return f'#{r:02x}{g:02x}{b:02x}'
        except:
            pass
        return '#007bff'

    def setup_site_config(self, soup):
        """Setup site configuration based on scraped data."""
        colors = self.extract_colors(soup)

        # Get or create site configuration
        config, created = SiteConfiguration.objects.get_or_create(id=1)

        # Extract site name
        title_tag = soup.find('title')
        if title_tag:
            config.site_name = title_tag.string.strip() if title_tag.string else 'Arhiva de Facturi'
        else:
            config.site_name = 'Arhiva de Facturi'

        # Set colors
        config.primary_color = colors['primary']
        config.secondary_color = colors['secondary']
        config.text_color = colors['text']
        config.background_color = colors['background']

        # Extract and download logo
        logo = soup.find('img', class_=re.compile('logo', re.I)) or soup.find('img', alt=re.compile('logo', re.I))
        if logo and logo.get('src'):
            media = self.download_image(logo['src'])
            if media:
                config.logo = media.file

        # Extract footer
        footer = soup.find('footer')
        if footer:
            config.footer_text = str(footer)
            config.footer_background_color = '#343a40'
            config.footer_text_color = '#ffffff'

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            config.default_meta_description = meta_desc.get('content', '')

        config.save()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Site configured: {config.site_name}'))

    def clone_homepage(self, soup):
        """Clone the homepage structure."""
        # Create or get homepage
        homepage, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Home',
                'status': 'published',
                'is_home': True,
                'order': 0,
                'created_by': self.user,
                'updated_by': self.user,
            }
        )

        if not created:
            homepage.sections.all().delete()

        # Extract meta information
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            homepage.meta_title = title_tag.string.strip()

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            homepage.meta_description = meta_desc.get('content', '')

        homepage.save()

        # Parse sections
        self.parse_sections(soup, homepage)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Homepage created with {homepage.sections.count()} sections'))

    def parse_sections(self, soup, page):
        """Parse and create sections from the page."""
        section_order = 0

        # Find main content
        main_content = soup.find('main') or soup.find('div', id='content') or soup.body

        if not main_content:
            return

        # Look for sections
        sections = main_content.find_all('section', limit=10)

        if not sections:
            # Try to find container divs
            sections = main_content.find_all('div', class_=re.compile('container|section|block', re.I), limit=10)

        for section_elem in sections:
            self.create_section_from_element(page, section_elem, section_order)
            section_order += 1

    def create_section_from_element(self, page, element, order):
        """Create a CMS section from an HTML element."""
        # Determine section type
        section_type = 'text'
        classes = element.get('class', [])
        class_str = ' '.join(classes).lower() if classes else ''

        if 'hero' in class_str or order == 0:
            section_type = 'hero'
        elif 'feature' in class_str:
            section_type = 'features'
        elif 'gallery' in class_str:
            section_type = 'gallery'
        elif 'contact' in class_str:
            section_type = 'contact'
        elif 'cta' in class_str:
            section_type = 'cta'

        # Extract title
        title_elem = element.find(['h1', 'h2', 'h3'])
        title = title_elem.get_text(strip=True) if title_elem else f'Section {order + 1}'

        # Create anchor ID
        anchor_id = re.sub(r'[^a-z0-9]+', '-', title.lower())[:50].strip('-')

        # Create section
        section = Section.objects.create(
            page=page,
            section_type=section_type,
            title=title,
            anchor_id=anchor_id,
            is_visible=True,
            padding_top=60,
            padding_bottom=60,
            order=order
        )

        # Parse content blocks
        self.parse_content_blocks(element, section)

        self.stdout.write(self.style.SUCCESS(f'    ✓ Section: {title} ({section_type})'))

    def parse_content_blocks(self, element, section):
        """Parse and create content blocks."""
        block_order = 0

        # Get all text paragraphs
        paragraphs = element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'], limit=10)
        if paragraphs:
            content = ''.join([str(p) for p in paragraphs])
            ContentBlock.objects.create(
                section=section,
                block_type='rich_text',
                content=content,
                order=block_order
            )
            block_order += 1

        # Get images
        images = element.find_all('img', limit=3)
        for img in images:
            src = img.get('src')
            if src:
                media = self.download_image(src)
                if media:
                    ContentBlock.objects.create(
                        section=section,
                        block_type='image',
                        image=media.file,
                        image_alt=img.get('alt', ''),
                        order=block_order
                    )
                    block_order += 1

        # Get buttons
        buttons = element.find_all('a', class_=re.compile('btn|button', re.I), limit=2)
        for btn in buttons:
            text = btn.get_text(strip=True)
            if text:
                ContentBlock.objects.create(
                    section=section,
                    block_type='button',
                    link_text=text,
                    link_url=btn.get('href', '#'),
                    button_style='primary',
                    order=block_order
                )
                block_order += 1

    def setup_navigation(self, soup):
        """Setup navigation menu."""
        MenuItem.objects.all().delete()

        nav = soup.find('nav') or soup.find('ul', class_=re.compile('nav|menu', re.I))
        if not nav:
            return

        links = nav.find_all('a', limit=8)
        order = 0

        for link in links:
            text = link.get_text(strip=True)
            href = link.get('href', '#')

            if not text:
                continue

            MenuItem.objects.create(
                label=text,
                link_type='external',
                external_url=href,
                is_visible=True,
                order=order
            )
            order += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {order} menu items'))
