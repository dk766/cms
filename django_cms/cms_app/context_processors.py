"""
Context processors for making data available to all templates.
"""
from .models import SiteConfiguration, MenuItem


def site_config(request):
    """
    Add site configuration and menu items to template context.
    """
    try:
        config = SiteConfiguration.objects.first()
        if not config:
            config = SiteConfiguration.objects.create()
    except Exception:
        config = None

    menu_items = MenuItem.objects.filter(is_visible=True, parent=None).prefetch_related('children')

    return {
        'site_config': config,
        'main_menu': menu_items,
    }
