"""
URL configuration for CMS API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PageViewSet, SectionViewSet, ContentBlockViewSet,
    MenuItemViewSet, MediaViewSet, SiteConfigurationViewSet
)

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'content-blocks', ContentBlockViewSet, basename='contentblock')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'site-config', SiteConfigurationViewSet, basename='siteconfig')

urlpatterns = [
    path('', include(router.urls)),
]
