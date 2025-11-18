"""
URL configuration for CMS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from cms_app.sitemaps import PageSitemap

sitemaps = {
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include('cms_app.backend_urls')),
    path('api/', include('cms_app.api.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('cms_app.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "CMS Administration"
admin.site.site_title = "CMS Admin Portal"
admin.site.index_title = "Welcome to CMS Administration"
