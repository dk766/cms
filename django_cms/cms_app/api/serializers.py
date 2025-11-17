"""
Serializers for CMS API.
"""
from rest_framework import serializers
from cms_app.models import (
    Page, Section, ContentBlock, MenuItem,
    Media, SiteConfiguration, GalleryImage
)


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for gallery images."""
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'alt_text', 'caption', 'order']


class ContentBlockSerializer(serializers.ModelSerializer):
    """Serializer for content blocks."""
    gallery_images = GalleryImageSerializer(many=True, read_only=True)
    block_type_display = serializers.CharField(source='get_block_type_display', read_only=True)

    class Meta:
        model = ContentBlock
        fields = [
            'id', 'block_type', 'block_type_display', 'title',
            'content', 'html_content', 'image', 'image_alt',
            'link_url', 'link_text', 'link_target', 'button_style',
            'background_color', 'text_color', 'config', 'order',
            'gallery_images'
        ]


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for sections."""
    content_blocks = ContentBlockSerializer(many=True, read_only=True)
    section_type_display = serializers.CharField(source='get_section_type_display', read_only=True)

    class Meta:
        model = Section
        fields = [
            'id', 'section_type', 'section_type_display', 'title',
            'anchor_id', 'is_visible', 'background_color',
            'background_image', 'text_color', 'padding_top',
            'padding_bottom', 'css_class', 'config', 'order',
            'content_blocks'
        ]


class PageListSerializer(serializers.ModelSerializer):
    """Serializer for page list (without sections)."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'meta_title', 'meta_description',
            'status', 'status_display', 'is_home', 'order',
            'created_at', 'updated_at', 'url'
        ]


class PageDetailSerializer(serializers.ModelSerializer):
    """Serializer for page detail (with sections)."""
    sections = SectionSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'meta_title', 'meta_description',
            'status', 'status_display', 'is_home', 'order', 'og_image',
            'created_at', 'updated_at', 'url', 'sections'
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for menu items."""
    children = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_url', read_only=True)
    link_type_display = serializers.CharField(source='get_link_type_display', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'label', 'link_type', 'link_type_display',
            'url', 'is_visible', 'order', 'children'
        ]

    def get_children(self, obj):
        """Get child menu items."""
        children = obj.children.filter(is_visible=True)
        return MenuItemSerializer(children, many=True).data


class MediaSerializer(serializers.ModelSerializer):
    """Serializer for media files."""
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            'id', 'title', 'file', 'file_url', 'media_type',
            'media_type_display', 'alt_text', 'caption',
            'file_size', 'width', 'height', 'tags',
            'uploaded_at', 'thumbnail_url'
        ]

    def get_file_url(self, obj):
        """Get full URL for file."""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def get_thumbnail_url(self, obj):
        """Get thumbnail URL for images."""
        request = self.context.get('request')
        if obj.media_type == 'image' and obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class SiteConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for site configuration."""
    class Meta:
        model = SiteConfiguration
        fields = [
            'id', 'site_name', 'logo', 'favicon',
            'primary_color', 'secondary_color', 'text_color',
            'background_color', 'font_family', 'base_font_size',
            'footer_text', 'footer_background_color', 'footer_text_color',
            'default_meta_description', 'facebook_url', 'twitter_url',
            'linkedin_url', 'instagram_url'
        ]
