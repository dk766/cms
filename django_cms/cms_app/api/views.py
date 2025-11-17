"""
API views for CMS.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from cms_app.models import (
    Page, Section, ContentBlock, MenuItem,
    Media, SiteConfiguration
)
from .serializers import (
    PageListSerializer, PageDetailSerializer, SectionSerializer,
    ContentBlockSerializer, MenuItemSerializer, MediaSerializer,
    SiteConfigurationSerializer
)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for pages.

    list: Get all published pages
    retrieve: Get a single page with all sections and content blocks
    """
    queryset = Page.objects.filter(status='published')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_home', 'status']
    search_fields = ['title', 'meta_description']
    ordering_fields = ['order', 'created_at', 'updated_at']
    ordering = ['order']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return PageListSerializer
        return PageDetailSerializer

    @action(detail=False, methods=['get'])
    def homepage(self, request):
        """Get the homepage."""
        page = Page.objects.filter(is_home=True, status='published').first()
        if not page:
            page = Page.objects.filter(status='published').first()

        if page:
            serializer = PageDetailSerializer(page, context={'request': request})
            return Response(serializer.data)

        return Response(
            {'error': 'No homepage found'},
            status=status.HTTP_404_NOT_FOUND
        )


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for sections.
    """
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['page', 'section_type', 'is_visible']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_queryset(self):
        """Filter visible sections for unauthenticated users."""
        queryset = Section.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_visible=True, page__status='published')
        return queryset.prefetch_related('content_blocks', 'content_blocks__gallery_images')


class ContentBlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for content blocks.
    """
    serializer_class = ContentBlockSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['section', 'block_type']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_queryset(self):
        """Filter blocks from visible sections for unauthenticated users."""
        queryset = ContentBlock.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(
                section__is_visible=True,
                section__page__status='published'
            )
        return queryset.prefetch_related('gallery_images')


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for menu items.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        """Only show visible top-level menu items."""
        return MenuItem.objects.filter(
            is_visible=True,
            parent=None
        ).prefetch_related('children')


class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for media files.
    """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['media_type']
    search_fields = ['title', 'alt_text', 'tags']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for site configuration.
    """
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current site configuration."""
        config = SiteConfiguration.objects.first()
        if config:
            serializer = SiteConfigurationSerializer(config, context={'request': request})
            return Response(serializer.data)

        return Response(
            {'error': 'Site configuration not found'},
            status=status.HTTP_404_NOT_FOUND
        )
