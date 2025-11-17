"""
Django admin configuration for CMS.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from import_export.admin import ImportExportModelAdmin
from .models import (
    SiteConfiguration, Page, Section, ContentBlock,
    MenuItem, Media, GalleryImage
)


class ContentBlockInline(SortableInlineAdminMixin, admin.TabularInline):
    """Inline admin for content blocks within sections."""
    model = ContentBlock
    extra = 0
    fields = [
        'block_type', 'title', 'content', 'image', 'link_url',
        'link_text', 'button_style', 'order'
    ]
    ordering = ['order']
    classes = ['collapse']


class GalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    """Inline admin for gallery images."""
    model = GalleryImage
    extra = 0
    fields = ['image', 'alt_text', 'caption', 'order']
    ordering = ['order']


class SectionInline(SortableInlineAdminMixin, admin.StackedInline):
    """Inline admin for sections within pages."""
    model = Section
    extra = 0
    fields = [
        'section_type', 'title', 'anchor_id', 'is_visible',
        'background_color', 'background_image', 'text_color',
        'padding_top', 'padding_bottom', 'css_class', 'order'
    ]
    ordering = ['order']
    classes = ['collapse']


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin for site-wide configuration."""
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name',)
        }),
        ('Branding', {
            'fields': ('logo', 'favicon'),
            'classes': ('collapse',)
        }),
        ('Colors', {
            'fields': (
                'primary_color', 'secondary_color',
                'text_color', 'background_color'
            ),
            'classes': ('collapse',)
        }),
        ('Typography', {
            'fields': ('font_family', 'base_font_size'),
            'classes': ('collapse',)
        }),
        ('Footer', {
            'fields': (
                'footer_text', 'footer_background_color',
                'footer_text_color'
            ),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('default_meta_description', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': (
                'facebook_url', 'twitter_url',
                'linkedin_url', 'instagram_url'
            ),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one site configuration
        if SiteConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of site configuration
        return False


@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Admin for pages."""
    list_display = [
        'title', 'slug', 'status', 'is_home',
        'order', 'section_count', 'preview_link', 'updated_at'
    ]
    list_filter = ['status', 'is_home', 'created_at', 'updated_at']
    search_fields = ['title', 'slug', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'status', 'is_home', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )

    def section_count(self, obj):
        """Display count of sections."""
        count = obj.sections.count()
        return format_html(
            '<span style="color: #007bff;">{} sections</span>',
            count
        )
    section_count.short_description = 'Sections'

    def preview_link(self, obj):
        """Display preview link."""
        if obj.pk:
            url = obj.get_absolute_url()
            return format_html(
                '<a href="{}" target="_blank" style="color: #28a745;">Preview →</a>',
                url
            )
        return '-'
    preview_link.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        """Save the model and track who created/updated it."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Admin for sections."""
    list_display = [
        'page', 'section_type', 'title', 'anchor_id',
        'is_visible', 'block_count', 'order'
    ]
    list_filter = ['section_type', 'is_visible', 'page']
    search_fields = ['title', 'anchor_id', 'page__title']
    inlines = [ContentBlockInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('page', 'section_type', 'title', 'anchor_id', 'is_visible', 'order')
        }),
        ('Styling', {
            'fields': (
                'background_color', 'background_image', 'text_color',
                'padding_top', 'padding_bottom', 'css_class'
            ),
            'classes': ('collapse',)
        }),
        ('Advanced Configuration', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
    )

    def block_count(self, obj):
        """Display count of content blocks."""
        count = obj.content_blocks.count()
        return format_html(
            '<span style="color: #007bff;">{} blocks</span>',
            count
        )
    block_count.short_description = 'Content Blocks'


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    """Admin for content blocks."""
    list_display = [
        'section', 'block_type', 'title_preview',
        'has_image', 'has_link', 'order'
    ]
    list_filter = ['block_type', 'section__page']
    search_fields = ['title', 'content', 'section__title']
    inlines = [GalleryImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('section', 'block_type', 'title', 'order')
        }),
        ('Content', {
            'fields': ('content', 'html_content'),
        }),
        ('Media', {
            'fields': ('image', 'image_alt'),
            'classes': ('collapse',)
        }),
        ('Link/Button', {
            'fields': ('link_url', 'link_text', 'link_target', 'button_style'),
            'classes': ('collapse',)
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        }),
        ('Advanced Configuration', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
    )

    def title_preview(self, obj):
        """Display title or truncated content."""
        if obj.title:
            return obj.title
        elif obj.content:
            return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return f'{obj.get_block_type_display()}'
    title_preview.short_description = 'Content Preview'

    def has_image(self, obj):
        """Show if block has an image."""
        if obj.image:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_image.short_description = 'Image'

    def has_link(self, obj):
        """Show if block has a link."""
        if obj.link_url:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_link.short_description = 'Link'


@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Admin for menu items."""
    list_display = [
        'label', 'link_type', 'get_target',
        'parent', 'is_visible', 'order'
    ]
    list_filter = ['link_type', 'is_visible', 'parent']
    search_fields = ['label', 'external_url']

    fieldsets = (
        ('Basic Information', {
            'fields': ('label', 'link_type', 'parent', 'is_visible', 'order')
        }),
        ('Link Target', {
            'fields': ('page', 'section', 'external_url'),
            'description': 'Select the appropriate field based on link type'
        }),
    )

    def get_target(self, obj):
        """Display the link target."""
        if obj.link_type == 'page' and obj.page:
            return obj.page.title
        elif obj.link_type == 'section' and obj.section:
            return f"{obj.section.page.title} → {obj.section.title or 'Section'}"
        elif obj.link_type == 'external' and obj.external_url:
            return obj.external_url
        return '-'
    get_target.short_description = 'Links To'


@admin.register(Media)
class MediaAdmin(ImportExportModelAdmin):
    """Admin for media library."""
    list_display = [
        'thumbnail_preview', 'title', 'media_type',
        'file_size_display', 'dimensions', 'uploaded_at', 'uploaded_by'
    ]
    list_filter = ['media_type', 'uploaded_at']
    search_fields = ['title', 'alt_text', 'tags']
    readonly_fields = ['file_size', 'width', 'height', 'uploaded_at', 'uploaded_by']

    fieldsets = (
        ('File Upload', {
            'fields': ('title', 'file')
        }),
        ('Metadata', {
            'fields': ('alt_text', 'caption', 'tags'),
        }),
        ('File Information', {
            'fields': ('media_type', 'file_size', 'width', 'height', 'uploaded_at', 'uploaded_by'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        """Display thumbnail for images."""
        if obj.media_type == 'image' and obj.file:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.file.url
            )
        return format_html('<span>📄 {}</span>', obj.media_type.upper())
    thumbnail_preview.short_description = 'Preview'

    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size:
            size = obj.file_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return '-'
    file_size_display.short_description = 'File Size'

    def dimensions(self, obj):
        """Display image dimensions."""
        if obj.width and obj.height:
            return f"{obj.width} × {obj.height}"
        return '-'
    dimensions.short_description = 'Dimensions'

    def save_model(self, request, obj, form, change):
        """Save the model and track who uploaded it."""
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


# Customize admin site
admin.site.site_header = "CMS Administration"
admin.site.site_title = "CMS Admin"
admin.site.index_title = "Content Management System"
