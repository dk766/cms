"""
Signal handlers for CMS app.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Page, Section, ContentBlock, MenuItem, SiteConfiguration


@receiver([post_save, post_delete], sender=Page)
@receiver([post_save, post_delete], sender=Section)
@receiver([post_save, post_delete], sender=ContentBlock)
@receiver([post_save, post_delete], sender=MenuItem)
@receiver([post_save, post_delete], sender=SiteConfiguration)
def clear_cache_on_change(sender, instance, **kwargs):
    """Clear cache when content changes."""
    cache.clear()
