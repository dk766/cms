"""
Django management command to clone https://info.arhivadefacturi.ro/ website.
This script scrapes the site and recreates it in the CMS.

Usage: python manage.py clone_arhiva_site
"""
import os
import re
import requests
from urllib.parse import urljoin, urlparse
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
from cms_app.models import (
    SiteConfiguration, Page, Section, ContentBlock, MenuItem, Media
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Clones https://info.arhivadefacturi.ro/ website into the CMS'

    def __init__(self):
        super().__init__()
        self.base_url = 'https://info.arhivadefacturi.ro'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.downloaded_images = {}
        self.user = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Skip downloading images',
        )

    def handle(self, *args, **options):
        self.skip_images = options.get('skip_images', False)

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('  Cloning https://info.arhivadefacturi.ro/'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Get or create admin user
        self.user = User.objects.filter(is_superuser=True).first()
        if not self.user:
            self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
            return

        try:
            # Step 1: Fetch and parse the homepage
            self.stdout.write('Step 1: Fetching homepage...')
            soup = self.fetch_page(self.base_url)
            if not soup:
                self.stdout.write(self.style.ERROR('Failed to fetch homepage'))
                return

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

    def fetch_page(self, url):
        """Fetch and parse a web page."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to fetch {url}: {str(e)}'))
            return None

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

            # Download image
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

        # Try to extract from inline styles or CSS
        for style_tag in soup.find_all('style'):
            style_content = style_tag.string
            if style_content:
                # Look for color definitions
                primary_match = re.search(r'--primary[:\s]+([#\w]+)', style_content)
                if primary_match:
                    colors['primary'] = primary_match.group(1)

        return colors

    def setup_site_config(self, soup):
        """Setup site configuration based on scraped data."""
        colors = self.extract_colors(soup)

        # Get or create site configuration
        config, created = SiteConfiguration.objects.get_or_create(id=1)

        # Extract site name
        title_tag = soup.find('title')
        if title_tag:
            config.site_name = title_tag.string.strip()
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
            # Clean up footer HTML
            footer_html = str(footer)
            config.footer_text = footer_html
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
            # Clear existing sections if page exists
            homepage.sections.all().delete()

        # Extract meta information
        title_tag = soup.find('title')
        if title_tag:
            homepage.meta_title = title_tag.string.strip()

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            homepage.meta_description = meta_desc.get('content', '')

        homepage.save()

        # Parse sections from the page
        self.parse_sections(soup, homepage)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Homepage created with {homepage.sections.count()} sections'))

    def parse_sections(self, soup, page):
        """Parse and create sections from the page."""
        section_order = 0

        # Try to identify main content sections
        main_content = soup.find('main') or soup.find('div', class_=re.compile('content|main', re.I)) or soup.body

        if not main_content:
            self.stdout.write(self.style.WARNING('  No main content found'))
            return

        # Look for common section patterns
        sections = main_content.find_all(['section', 'div'], class_=re.compile('section|block|hero|feature|about|contact', re.I))

        if not sections:
            # Fallback: treat major divs as sections
            sections = main_content.find_all('div', recursive=False)

        for idx, section_elem in enumerate(sections[:10]):  # Limit to 10 sections
            self.create_section_from_element(page, section_elem, section_order)
            section_order += 1

        # If no sections found, create a generic content section
        if section_order == 0:
            self.create_generic_section(page, main_content)

    def create_section_from_element(self, page, element, order):
        """Create a CMS section from an HTML element."""
        # Determine section type
        section_type = 'text'
        classes = element.get('class', [])
        class_str = ' '.join(classes).lower()

        if 'hero' in class_str or 'banner' in class_str or 'jumbotron' in class_str:
            section_type = 'hero'
        elif 'feature' in class_str or 'service' in class_str:
            section_type = 'features'
        elif 'gallery' in class_str or 'portfolio' in class_str:
            section_type = 'gallery'
        elif 'testimonial' in class_str:
            section_type = 'testimonials'
        elif 'contact' in class_str:
            section_type = 'contact'
        elif 'faq' in class_str:
            section_type = 'faq'
        elif 'cta' in class_str or 'call-to-action' in class_str:
            section_type = 'cta'

        # Extract title
        title_elem = element.find(['h1', 'h2', 'h3'])
        title = title_elem.get_text(strip=True) if title_elem else f'Section {order + 1}'

        # Create anchor ID
        anchor_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        # Extract background color/image
        bg_color = None
        bg_image = None
        style = element.get('style', '')
        if 'background-color' in style:
            color_match = re.search(r'background-color:\s*([^;]+)', style)
            if color_match:
                bg_color = color_match.group(1).strip()

        bg_img_elem = element.find('img', class_=re.compile('background|bg', re.I))
        if bg_img_elem:
            media = self.download_image(bg_img_elem['src'])
            if media:
                bg_image = media.file

        # Create section
        section = Section.objects.create(
            page=page,
            section_type=section_type,
            title=title,
            anchor_id=anchor_id,
            is_visible=True,
            background_color=bg_color,
            order=order
        )

        if bg_image:
            section.background_image = bg_image
            section.save()

        # Parse content blocks
        self.parse_content_blocks(element, section)

        self.stdout.write(self.style.SUCCESS(f'    ✓ Section created: {title} ({section_type})'))

    def parse_content_blocks(self, element, section):
        """Parse and create content blocks from a section element."""
        block_order = 0

        # Extract text content
        text_content = []
        for child in element.children:
            if hasattr(child, 'name'):
                if child.name in ['p', 'div', 'span']:
                    text = child.get_text(strip=True)
                    if text and len(text) > 10:
                        text_content.append(str(child))

        if text_content:
            ContentBlock.objects.create(
                section=section,
                block_type='rich_text',
                content=''.join(text_content),
                order=block_order
            )
            block_order += 1

        # Extract images
        images = element.find_all('img', limit=5)
        for img in images:
            src = img.get('src')
            if src and not self.is_background_image(img):
                media = self.download_image(src)
                if media:
                    ContentBlock.objects.create(
                        section=section,
                        block_type='image',
                        image=media.file,
                        image_alt=img.get('alt', ''),
                        title=img.get('title', ''),
                        order=block_order
                    )
                    block_order += 1

        # Extract buttons/links
        buttons = element.find_all('a', class_=re.compile('btn|button|cta', re.I), limit=3)
        for btn in buttons:
            href = btn.get('href', '#')
            text = btn.get_text(strip=True)
            if text:
                ContentBlock.objects.create(
                    section=section,
                    block_type='button',
                    link_text=text,
                    link_url=href,
                    button_style='primary',
                    order=block_order
                )
                block_order += 1

    def is_background_image(self, img):
        """Check if an image is likely a background image."""
        classes = img.get('class', [])
        class_str = ' '.join(classes).lower()
        return 'background' in class_str or 'bg' in class_str or 'hero-bg' in class_str

    def create_generic_section(self, page, content):
        """Create a generic section with all content."""
        section = Section.objects.create(
            page=page,
            section_type='text',
            title='Main Content',
            order=0
        )

        # Get all text content
        text_elements = content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol'])
        content_html = ''.join([str(elem) for elem in text_elements[:20]])

        if content_html:
            ContentBlock.objects.create(
                section=section,
                block_type='rich_text',
                content=content_html,
                order=0
            )

    def setup_navigation(self, soup):
        """Setup navigation menu from the site."""
        # Clear existing menu items
        MenuItem.objects.all().delete()

        # Find navigation
        nav = soup.find('nav') or soup.find('div', class_=re.compile('nav|menu', re.I))
        if not nav:
            self.stdout.write(self.style.WARNING('  No navigation found'))
            return

        # Extract menu items
        links = nav.find_all('a', limit=10)
        order = 0

        for link in links:
            text = link.get_text(strip=True)
            href = link.get('href', '#')

            if not text or text.lower() in ['login', 'signup', 'register']:
                continue

            # Determine link type
            if href.startswith('#'):
                # Section link - we'll link to homepage for now
                MenuItem.objects.create(
                    label=text,
                    link_type='external',
                    external_url=href,
                    is_visible=True,
                    order=order
                )
            elif href.startswith('http'):
                # External link
                MenuItem.objects.create(
                    label=text,
                    link_type='external',
                    external_url=href,
                    is_visible=True,
                    order=order
                )
            else:
                # Internal page (we'll create as external for now)
                MenuItem.objects.create(
                    label=text,
                    link_type='external',
                    external_url=href,
                    is_visible=True,
                    order=order
                )

            order += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {order} menu items'))
