"""
Backend editor views for CMS.
Provides a user-friendly visual editor interface.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import (
    Page, Section, ContentBlock, MenuItem,
    Media, SiteConfiguration, GalleryImage
)


class EditorPermissionMixin(LoginRequiredMixin):
    """Mixin to check if user has editor permissions."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Allow superusers and staff with specific permissions
        if not (request.user.is_superuser or
                request.user.has_perm('cms_app.change_page') or
                request.user.groups.filter(name='Editors').exists()):
            return HttpResponseForbidden("You don't have permission to access the backend editor.")

        return super().dispatch(request, *args, **kwargs)


class BackendDashboardView(EditorPermissionMixin, TemplateView):
    """Backend editor dashboard."""
    template_name = 'cms_app/backend/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pages'] = Page.objects.count()
        context['published_pages'] = Page.objects.filter(status='published').count()
        context['draft_pages'] = Page.objects.filter(status='draft').count()
        context['total_media'] = Media.objects.count()
        context['recent_pages'] = Page.objects.all().order_by('-updated_at')[:5]
        return context


class BackendPageListView(EditorPermissionMixin, ListView):
    """List all pages in the backend."""
    model = Page
    template_name = 'cms_app/backend/page_list.html'
    context_object_name = 'pages'
    paginate_by = 20

    def get_queryset(self):
        queryset = Page.objects.all().order_by('-updated_at')

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(slug__icontains=search) |
                Q(meta_description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class BackendPageEditorView(EditorPermissionMixin, DetailView):
    """Visual page editor."""
    model = Page
    template_name = 'cms_app/backend/page_editor.html'
    context_object_name = 'page'
    pk_url_kwarg = 'page_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object

        # Get all sections with their content blocks (including hidden ones for editing)
        sections = page.sections.all().prefetch_related(
            'content_blocks',
            'content_blocks__gallery_images'
        ).order_by('order')

        context['sections'] = sections
        context['section_types'] = Section.SECTION_TYPE_CHOICES
        context['block_types'] = ContentBlock.BLOCK_TYPE_CHOICES

        return context


class BackendPageCreateView(EditorPermissionMixin, View):
    """Create a new page."""

    def get(self, request):
        """Show page creation form."""
        context = {
            'section_types': Section.SECTION_TYPE_CHOICES,
            'block_types': ContentBlock.BLOCK_TYPE_CHOICES,
        }
        return render(request, 'cms_app/backend/page_create.html', context)

    def post(self, request):
        """Create a new page."""
        try:
            page = Page.objects.create(
                title=request.POST.get('title', 'New Page'),
                slug=request.POST.get('slug', ''),
                status='draft',
                created_by=request.user,
                updated_by=request.user
            )

            return redirect('backend_page_editor', page_id=page.id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class BackendMediaLibraryView(EditorPermissionMixin, ListView):
    """Media library for backend."""
    model = Media
    template_name = 'cms_app/backend/media_library.html'
    context_object_name = 'media_files'
    paginate_by = 24

    def get_queryset(self):
        queryset = Media.objects.all().order_by('-uploaded_at')

        # Filter by type
        media_type = self.request.GET.get('type')
        if media_type:
            queryset = queryset.filter(media_type=media_type)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(tags__icontains=search) |
                Q(alt_text__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class BackendSettingsView(EditorPermissionMixin, View):
    """Site settings editor."""

    def get(self, request):
        """Show settings form."""
        config, created = SiteConfiguration.objects.get_or_create()
        return render(request, 'cms_app/backend/settings.html', {'config': config})

    def post(self, request):
        """Save settings."""
        config, created = SiteConfiguration.objects.get_or_create()

        # Update configuration fields
        config.site_name = request.POST.get('site_name', '')
        config.primary_color = request.POST.get('primary_color', '#007bff')
        config.secondary_color = request.POST.get('secondary_color', '#6c757d')
        config.font_family = request.POST.get('font_family', 'Arial, sans-serif')
        config.base_font_size = request.POST.get('base_font_size', 16)
        config.default_meta_description = request.POST.get('default_meta_description', '')
        config.google_analytics_id = request.POST.get('google_analytics_id', '')
        config.facebook_url = request.POST.get('facebook_url', '')
        config.twitter_url = request.POST.get('twitter_url', '')
        config.linkedin_url = request.POST.get('linkedin_url', '')
        config.instagram_url = request.POST.get('instagram_url', '')
        config.footer_text = request.POST.get('footer_text', '')

        config.save()

        from django.contrib import messages
        messages.success(request, 'Settings saved successfully!')

        return redirect('backend_settings')


# AJAX API Views for the backend editor

@login_required
@require_http_methods(["POST"])
def ajax_save_page(request, page_id):
    """Save page details via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.change_page') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        page = get_object_or_404(Page, id=page_id)
        data = json.loads(request.body)

        # Update page fields
        if 'title' in data:
            page.title = data['title']
        if 'slug' in data:
            page.slug = data['slug']
        if 'status' in data:
            page.status = data['status']
        if 'is_home' in data:
            page.is_home = data['is_home']
        if 'meta_title' in data:
            page.meta_title = data['meta_title']
        if 'meta_description' in data:
            page.meta_description = data['meta_description']

        page.updated_by = request.user
        page.save()

        return JsonResponse({
            'success': True,
            'message': 'Page saved successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_create_section(request, page_id):
    """Create a new section via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.add_section') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        page = get_object_or_404(Page, id=page_id)
        data = json.loads(request.body)

        # Get the max order for this page
        max_order = page.sections.count()

        section = Section.objects.create(
            page=page,
            section_type=data.get('section_type', 'text'),
            title=data.get('title', ''),
            order=data.get('order', max_order)
        )

        return JsonResponse({
            'success': True,
            'section_id': section.id,
            'message': 'Section created successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_update_section(request, section_id):
    """Update section via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.change_section') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        section = get_object_or_404(Section, id=section_id)
        data = json.loads(request.body)

        # Update section fields
        for field in ['title', 'section_type', 'anchor_id', 'is_visible',
                      'background_color', 'text_color', 'padding_top',
                      'padding_bottom', 'css_class', 'order']:
            if field in data:
                setattr(section, field, data[field])

        section.save()

        return JsonResponse({
            'success': True,
            'message': 'Section updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_delete_section(request, section_id):
    """Delete section via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.delete_section') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        section = get_object_or_404(Section, id=section_id)
        section.delete()

        return JsonResponse({
            'success': True,
            'message': 'Section deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_reorder_sections(request, page_id):
    """Reorder sections via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.change_section') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        page = get_object_or_404(Page, id=page_id)
        data = json.loads(request.body)
        section_orders = data.get('sections', [])

        with transaction.atomic():
            for item in section_orders:
                Section.objects.filter(
                    id=item['id'],
                    page=page
                ).update(order=item['order'])

        return JsonResponse({
            'success': True,
            'message': 'Sections reordered successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_create_block(request, section_id):
    """Create a new content block via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.add_contentblock') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        section = get_object_or_404(Section, id=section_id)
        data = json.loads(request.body)

        # Get the max order for this section
        max_order = section.content_blocks.count()

        block = ContentBlock.objects.create(
            section=section,
            block_type=data.get('block_type', 'text'),
            title=data.get('title', ''),
            content=data.get('content', ''),
            order=data.get('order', max_order)
        )

        return JsonResponse({
            'success': True,
            'block_id': block.id,
            'message': 'Content block created successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_update_block(request, block_id):
    """Update content block via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.change_contentblock') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        block = get_object_or_404(ContentBlock, id=block_id)
        data = json.loads(request.body)

        # Update block fields
        for field in ['title', 'content', 'html_content', 'block_type',
                      'image_alt', 'link_url', 'link_text', 'link_target',
                      'button_style', 'background_color', 'text_color', 'order']:
            if field in data:
                setattr(block, field, data[field])

        block.save()

        return JsonResponse({
            'success': True,
            'message': 'Content block updated successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_delete_block(request, block_id):
    """Delete content block via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.delete_contentblock') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        block = get_object_or_404(ContentBlock, id=block_id)
        block.delete()

        return JsonResponse({
            'success': True,
            'message': 'Content block deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_upload_media(request):
    """Upload media file via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.add_media') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']

        media = Media.objects.create(
            file=file,
            title=request.POST.get('title', file.name),
            alt_text=request.POST.get('alt_text', ''),
            uploaded_by=request.user
        )

        return JsonResponse({
            'success': True,
            'media_id': media.id,
            'url': media.file.url,
            'message': 'File uploaded successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def ajax_delete_page(request, page_id):
    """Delete a page via AJAX."""
    if not (request.user.is_superuser or
            request.user.has_perm('cms_app.delete_page') or
            request.user.groups.filter(name='Editors').exists()):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        page = get_object_or_404(Page, id=page_id)

        # Don't allow deleting the homepage
        if page.is_home:
            return JsonResponse({
                'error': 'Cannot delete the homepage. Set another page as home first.'
            }, status=400)

        page.delete()

        return JsonResponse({
            'success': True,
            'message': 'Page deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
