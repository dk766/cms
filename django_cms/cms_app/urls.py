"""
URL configuration for CMS app.
"""
from django.urls import path
from .views import HomePageView, PageDetailView, MediaLibraryView, robots_txt

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('media-library/', MediaLibraryView.as_view(), name='media_library'),
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
]
