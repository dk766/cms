"""
Sitemap configuration for SEO.
"""
from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):
    """Sitemap for pages."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """Return all published pages."""
        return Page.objects.filter(status='published')

    def lastmod(self, obj):
        """Return last modification date."""
        return obj.updated_at

    def location(self, obj):
        """Return page URL."""
        return obj.get_absolute_url()
