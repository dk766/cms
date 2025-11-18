"""
URL configuration for backend editor.
"""
from django.urls import path
from . import backend_views

urlpatterns = [
    # Dashboard
    path('', backend_views.BackendDashboardView.as_view(), name='backend_dashboard'),

    # Pages
    path('pages/', backend_views.BackendPageListView.as_view(), name='backend_page_list'),
    path('pages/create/', backend_views.BackendPageCreateView.as_view(), name='backend_page_create'),
    path('pages/<int:page_id>/edit/', backend_views.BackendPageEditorView.as_view(), name='backend_page_editor'),

    # Media
    path('media/', backend_views.BackendMediaLibraryView.as_view(), name='backend_media_library'),

    # Settings
    path('settings/', backend_views.BackendSettingsView.as_view(), name='backend_settings'),

    # AJAX API endpoints
    path('api/pages/<int:page_id>/save/', backend_views.ajax_save_page, name='ajax_save_page'),
    path('api/pages/<int:page_id>/delete/', backend_views.ajax_delete_page, name='ajax_delete_page'),
    path('api/pages/<int:page_id>/sections/create/', backend_views.ajax_create_section, name='ajax_create_section'),
    path('api/pages/<int:page_id>/sections/reorder/', backend_views.ajax_reorder_sections, name='ajax_reorder_sections'),
    path('api/sections/<int:section_id>/update/', backend_views.ajax_update_section, name='ajax_update_section'),
    path('api/sections/<int:section_id>/delete/', backend_views.ajax_delete_section, name='ajax_delete_section'),
    path('api/sections/<int:section_id>/blocks/create/', backend_views.ajax_create_block, name='ajax_create_block'),
    path('api/blocks/<int:block_id>/update/', backend_views.ajax_update_block, name='ajax_update_block'),
    path('api/blocks/<int:block_id>/delete/', backend_views.ajax_delete_block, name='ajax_delete_block'),
    path('api/media/upload/', backend_views.ajax_upload_media, name='ajax_upload_media'),
]
