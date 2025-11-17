"""
Core models for Django CMS application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
import os
import json


class SiteConfiguration(models.Model):
    """
    Global site configuration for theming and branding.
    Should only have one instance.
    """
    site_name = models.CharField(max_length=200, default="My Website")

    # Branding
    logo = models.ImageField(upload_to='branding/', null=True, blank=True)
    favicon = models.ImageField(upload_to='branding/', null=True, blank=True)

    # Colors
    primary_color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    secondary_color = models.CharField(max_length=7, default='#6c757d', help_text='Hex color code')
    text_color = models.CharField(max_length=7, default='#212529', help_text='Hex color code')
    background_color = models.CharField(max_length=7, default='#ffffff', help_text='Hex color code')

    # Typography
    font_family = models.CharField(
        max_length=100,
        default='Arial, sans-serif',
        help_text='CSS font-family value'
    )
    base_font_size = models.IntegerField(default=16, help_text='Base font size in pixels')

    # Footer
    footer_text = RichTextField(blank=True, null=True)
    footer_background_color = models.CharField(max_length=7, default='#343a40')
    footer_text_color = models.CharField(max_length=7, default='#ffffff')

    # SEO
    default_meta_description = models.TextField(blank=True, null=True, max_length=160)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)

    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            return SiteConfiguration.objects.first()
        return super().save(*args, **kwargs)


class Page(models.Model):
    """
    Represents a page in the CMS.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=160, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_home = models.BooleanField(default=False, help_text='Set as homepage')

    # SEO
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)

    # Ordering
    order = models.IntegerField(default=0, help_text='Order in navigation')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pages_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pages_updated')

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.meta_title:
            self.meta_title = self.title

        # Ensure only one homepage
        if self.is_home:
            Page.objects.filter(is_home=True).exclude(pk=self.pk).update(is_home=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.is_home:
            return '/'
        return reverse('page_detail', kwargs={'slug': self.slug})


class Section(models.Model):
    """
    Represents a section within a page.
    """
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('text', 'Text Section'),
        ('image', 'Image Section'),
        ('gallery', 'Image Gallery'),
        ('two_column', 'Two Column Layout'),
        ('three_column', 'Three Column Layout'),
        ('carousel', 'Carousel/Slider'),
        ('cta', 'Call to Action'),
        ('faq', 'FAQ Section'),
        ('contact', 'Contact Section'),
        ('testimonials', 'Testimonials'),
        ('features', 'Features Grid'),
        ('custom', 'Custom Section'),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default='text')
    title = models.CharField(max_length=200, blank=True, null=True)
    anchor_id = models.SlugField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ID for linking to this section (e.g., #about)'
    )

    # Visibility
    is_visible = models.BooleanField(default=True)

    # Styling
    background_color = models.CharField(max_length=7, blank=True, null=True, help_text='Hex color code')
    background_image = models.ImageField(upload_to='section_backgrounds/', blank=True, null=True)
    text_color = models.CharField(max_length=7, blank=True, null=True, help_text='Hex color code')
    padding_top = models.IntegerField(default=60, help_text='Padding in pixels')
    padding_bottom = models.IntegerField(default=60, help_text='Padding in pixels')

    # Custom CSS classes
    css_class = models.CharField(max_length=200, blank=True, null=True)

    # Configuration stored as JSON
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional configuration options in JSON format'
    )

    # Ordering
    order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page', 'order']
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return f"{self.page.title} - {self.get_section_type_display()} ({self.order})"

    def save(self, *args, **kwargs):
        if not self.anchor_id and self.title:
            self.anchor_id = slugify(self.title)
        super().save(*args, **kwargs)


class ContentBlock(models.Model):
    """
    Represents a content block within a section.
    """
    BLOCK_TYPES = [
        ('rich_text', 'Rich Text'),
        ('heading', 'Heading'),
        ('image', 'Single Image'),
        ('gallery', 'Image Gallery'),
        ('video', 'Video Embed'),
        ('button', 'Button/CTA'),
        ('icon_text', 'Icon + Text'),
        ('code', 'Code Block'),
        ('spacer', 'Spacer'),
        ('divider', 'Divider'),
        ('html', 'Raw HTML'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='content_blocks')
    block_type = models.CharField(max_length=50, choices=BLOCK_TYPES, default='rich_text')

    # Content fields
    title = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextField(blank=True, null=True, help_text='Rich text content')
    html_content = models.TextField(blank=True, null=True, help_text='Raw HTML content')

    # Image
    image = models.ImageField(upload_to='content_blocks/', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True, null=True)

    # Link/Button
    link_url = models.CharField(max_length=500, blank=True, null=True)
    link_text = models.CharField(max_length=200, blank=True, null=True)
    link_target = models.CharField(
        max_length=20,
        choices=[('_self', 'Same window'), ('_blank', 'New window')],
        default='_self'
    )

    # Styling
    background_color = models.CharField(max_length=7, blank=True, null=True)
    text_color = models.CharField(max_length=7, blank=True, null=True)
    button_style = models.CharField(
        max_length=50,
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('success', 'Success'),
            ('danger', 'Danger'),
            ('warning', 'Warning'),
            ('info', 'Info'),
            ('light', 'Light'),
            ('dark', 'Dark'),
        ],
        default='primary'
    )

    # Configuration
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional configuration in JSON format'
    )

    # Ordering
    order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section', 'order']
        verbose_name = "Content Block"
        verbose_name_plural = "Content Blocks"

    def __str__(self):
        return f"{self.section} - {self.get_block_type_display()} ({self.order})"


class MenuItem(models.Model):
    """
    Represents an item in the navigation menu.
    """
    LINK_TYPES = [
        ('page', 'Internal Page'),
        ('section', 'Page Section'),
        ('external', 'External URL'),
    ]

    label = models.CharField(max_length=100)
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='page')

    # Link targets
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    external_url = models.CharField(max_length=500, blank=True, null=True)

    # Parent for dropdown menus
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # Visibility
    is_visible = models.BooleanField(default=True)

    # Ordering
    order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'label']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.label

    def get_url(self):
        """Get the URL for this menu item."""
        if self.link_type == 'page' and self.page:
            return self.page.get_absolute_url()
        elif self.link_type == 'section' and self.section:
            page_url = self.section.page.get_absolute_url()
            if self.section.anchor_id:
                return f"{page_url}#{self.section.anchor_id}"
            return page_url
        elif self.link_type == 'external' and self.external_url:
            return self.external_url
        return '#'


class Media(models.Model):
    """
    Media library for managing uploaded files.
    """
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image')

    # Metadata
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True, help_text='File size in bytes')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    # Organization
    tags = models.CharField(max_length=500, blank=True, null=True, help_text='Comma-separated tags')

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Media File"
        verbose_name_plural = "Media Library"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            # Determine media type from file extension
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                self.media_type = 'image'
            elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']:
                self.media_type = 'document'
            elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                self.media_type = 'video'
            else:
                self.media_type = 'other'

            # Get file size
            self.file_size = self.file.size

            # For images, get dimensions
            if self.media_type == 'image' and ext != '.svg':
                try:
                    img = Image.open(self.file)
                    self.width, self.height = img.size
                except Exception:
                    pass

        super().save(*args, **kwargs)

    def get_thumbnail_url(self):
        """Get thumbnail URL for images."""
        if self.media_type == 'image':
            return self.file.url
        return None


class GalleryImage(models.Model):
    """
    Images for gallery blocks.
    """
    content_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='galleries/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    caption = models.CharField(max_length=500, blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return f"Gallery image for {self.content_block}"
