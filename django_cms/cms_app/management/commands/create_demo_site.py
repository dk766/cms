"""
Management command to create demo site content.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cms_app.models import (
    SiteConfiguration, Page, Section, ContentBlock, MenuItem
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo site content for the CMS'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo site content...\n')

        # Get or create admin user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ Created admin user (username: admin, password: admin)'))

        # Create site configuration
        config, created = SiteConfiguration.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'Demo CMS Website',
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'text_color': '#212529',
                'background_color': '#ffffff',
                'font_family': 'Arial, sans-serif',
                'base_font_size': 16,
                'footer_text': '<p>© 2024 Demo CMS Website. All rights reserved.</p><p>Built with Django CMS</p>',
                'footer_background_color': '#343a40',
                'footer_text_color': '#ffffff',
                'default_meta_description': 'A powerful Django-based CMS for creating beautiful websites',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created site configuration'))

        # Create Homepage
        homepage, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Home',
                'meta_title': 'Welcome to Our Website',
                'meta_description': 'Discover our amazing products and services',
                'status': 'published',
                'is_home': True,
                'order': 0,
                'created_by': user,
                'updated_by': user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created homepage'))

            # Hero Section
            hero = Section.objects.create(
                page=homepage,
                section_type='hero',
                title='Welcome Section',
                anchor_id='welcome',
                background_color='#f8f9fa',
                padding_top=100,
                padding_bottom=100,
                order=0
            )
            ContentBlock.objects.create(
                section=hero,
                block_type='rich_text',
                content='<h1 class="display-3 fw-bold mb-4">Welcome to Our CMS</h1><p class="lead">Build beautiful websites with ease using our powerful content management system.</p>',
                order=0
            )
            ContentBlock.objects.create(
                section=hero,
                block_type='button',
                link_text='Get Started',
                link_url='#features',
                button_style='primary',
                order=1
            )

            # Features Section
            features = Section.objects.create(
                page=homepage,
                section_type='features',
                title='Features',
                anchor_id='features',
                padding_top=80,
                padding_bottom=80,
                order=1
            )
            feature_items = [
                ('Easy to Use', 'Intuitive admin interface that anyone can master', 'bi-star-fill'),
                ('Responsive Design', 'Mobile-first design that looks great on all devices', 'bi-phone-fill'),
                ('SEO Optimized', 'Built-in SEO features to help you rank higher', 'bi-graph-up'),
                ('Flexible Content', 'Multiple section and block types for any layout', 'bi-layout-text-window-reverse'),
                ('Media Library', 'Organized media management system', 'bi-images'),
                ('REST API', 'Full-featured API for headless CMS usage', 'bi-code-slash'),
            ]
            for i, (title, desc, icon) in enumerate(feature_items):
                ContentBlock.objects.create(
                    section=features,
                    block_type='icon_text',
                    title=title,
                    content=f'<p>{desc}</p>',
                    config={'icon': icon},
                    order=i
                )

            # CTA Section
            cta = Section.objects.create(
                page=homepage,
                section_type='cta',
                title='Ready to Get Started?',
                anchor_id='cta',
                background_color='#007bff',
                text_color='#ffffff',
                padding_top=80,
                padding_bottom=80,
                order=2
            )
            ContentBlock.objects.create(
                section=cta,
                block_type='rich_text',
                content='<h2>Start Building Your Website Today</h2><p class="lead">Join thousands of users who trust our CMS</p>',
                order=0
            )
            ContentBlock.objects.create(
                section=cta,
                block_type='button',
                link_text='Contact Us',
                link_url='/contact/',
                button_style='light',
                order=1
            )

        # Create About Page
        about, created = Page.objects.get_or_create(
            slug='about',
            defaults={
                'title': 'About Us',
                'meta_title': 'About Our Company',
                'meta_description': 'Learn more about our company and what we do',
                'status': 'published',
                'order': 1,
                'created_by': user,
                'updated_by': user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created about page'))

            about_section = Section.objects.create(
                page=about,
                section_type='two_column',
                title='Our Story',
                padding_top=80,
                padding_bottom=80,
                order=0
            )
            ContentBlock.objects.create(
                section=about_section,
                block_type='rich_text',
                content='<h2>Who We Are</h2><p>We are a team of passionate developers and designers dedicated to creating the best content management system for modern websites.</p><p>Our mission is to make website creation accessible to everyone, regardless of technical expertise.</p>',
                order=0
            )
            ContentBlock.objects.create(
                section=about_section,
                block_type='rich_text',
                content='<h2>What We Do</h2><p>We provide a powerful, flexible CMS that enables businesses and individuals to create stunning websites without writing code.</p><p>Our platform combines ease of use with advanced features, giving you the best of both worlds.</p>',
                order=1
            )

        # Create Services Page
        services, created = Page.objects.get_or_create(
            slug='services',
            defaults={
                'title': 'Services',
                'meta_title': 'Our Services',
                'meta_description': 'Explore our range of services',
                'status': 'published',
                'order': 2,
                'created_by': user,
                'updated_by': user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created services page'))

            services_section = Section.objects.create(
                page=services,
                section_type='three_column',
                title='What We Offer',
                padding_top=80,
                padding_bottom=80,
                order=0
            )
            service_items = [
                ('Website Development', 'Custom website solutions tailored to your needs'),
                ('Content Management', 'Easy-to-use CMS for managing your content'),
                ('SEO Optimization', 'Improve your search engine rankings'),
                ('Responsive Design', 'Websites that work on all devices'),
                ('API Integration', 'Connect your website with external services'),
                ('Technical Support', '24/7 support to help you succeed'),
            ]
            for i, (title, desc) in enumerate(service_items):
                ContentBlock.objects.create(
                    section=services_section,
                    block_type='rich_text',
                    content=f'<h3>{title}</h3><p>{desc}</p>',
                    order=i
                )

        # Create Contact Page
        contact, created = Page.objects.get_or_create(
            slug='contact',
            defaults={
                'title': 'Contact',
                'meta_title': 'Contact Us',
                'meta_description': 'Get in touch with us',
                'status': 'published',
                'order': 3,
                'created_by': user,
                'updated_by': user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created contact page'))

            contact_section = Section.objects.create(
                page=contact,
                section_type='contact',
                title='Get In Touch',
                padding_top=80,
                padding_bottom=80,
                order=0
            )
            ContentBlock.objects.create(
                section=contact_section,
                block_type='rich_text',
                content='''
                <h2>Contact Information</h2>
                <p><i class="bi bi-envelope-fill me-2"></i> Email: info@example.com</p>
                <p><i class="bi bi-telephone-fill me-2"></i> Phone: +1 (555) 123-4567</p>
                <p><i class="bi bi-geo-alt-fill me-2"></i> Address: 123 Main St, City, State 12345</p>
                <hr class="my-4">
                <p>We'd love to hear from you! Send us a message and we'll respond as soon as possible.</p>
                ''',
                order=0
            )

        # Create Navigation Menu
        menu_items = [
            ('Home', 'page', homepage, None, None, 0),
            ('About', 'page', about, None, None, 1),
            ('Services', 'page', services, None, None, 2),
            ('Contact', 'page', contact, None, None, 3),
        ]

        for label, link_type, page, section, parent, order in menu_items:
            MenuItem.objects.get_or_create(
                label=label,
                defaults={
                    'link_type': link_type,
                    'page': page,
                    'section': section,
                    'parent': parent,
                    'is_visible': True,
                    'order': order,
                }
            )
        self.stdout.write(self.style.SUCCESS('✓ Created navigation menu'))

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Demo site created successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('\n')
        self.stdout.write('Visit http://localhost:8000/ to see your demo site')
        self.stdout.write('Login to admin at http://localhost:8000/admin/')
        if created:
            self.stdout.write('  Username: admin')
            self.stdout.write('  Password: admin')
        self.stdout.write('\n')
