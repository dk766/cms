"""
Views for CMS application.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Page, Section, ContentBlock, Media


class HomePageView(DetailView):
    """Display the homepage."""
    model = Page
    template_name = 'cms_app/page.html'
    context_object_name = 'page'

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        """Get the homepage or first published page."""
        try:
            # Try to get the designated homepage
            page = Page.objects.filter(is_home=True, status='published').first()
            if not page:
                # Fallback to first published page
                page = Page.objects.filter(status='published').first()
            if not page:
                raise Http404("No published pages found")
            return page
        except Page.DoesNotExist:
            raise Http404("Homepage not found")

    def get_context_data(self, **kwargs):
        """Add sections and blocks to context."""
        context = super().get_context_data(**kwargs)
        page = self.object

        # Get all visible sections with their content blocks
        sections = page.sections.filter(is_visible=True).prefetch_related('content_blocks')
        context['sections'] = sections

        return context


class PageDetailView(DetailView):
    """Display a single page."""
    model = Page
    template_name = 'cms_app/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Only show published pages."""
        return Page.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        """Add sections and blocks to context."""
        context = super().get_context_data(**kwargs)
        page = self.object

        # Get all visible sections with their content blocks
        sections = page.sections.filter(is_visible=True).prefetch_related(
            'content_blocks',
            'content_blocks__gallery_images'
        )
        context['sections'] = sections

        return context


class MediaLibraryView(ListView):
    """Display media library (for authenticated users)."""
    model = Media
    template_name = 'cms_app/media_library.html'
    context_object_name = 'media_files'
    paginate_by = 24

    def get_queryset(self):
        """Get media files, optionally filtered."""
        queryset = Media.objects.all()

        # Filter by media type if specified
        media_type = self.request.GET.get('type')
        if media_type:
            queryset = queryset.filter(media_type=media_type)

        # Search by title or tags
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(tags__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """Add filter options to context."""
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


def robots_txt(request):
    """Serve robots.txt file."""
    content = """User-agent: *
Allow: /

Sitemap: {scheme}://{host}/sitemap.xml
""".format(
        scheme=request.scheme,
        host=request.get_host()
    )
    return render(request, 'cms_app/robots.txt', {'content': content}, content_type='text/plain')
