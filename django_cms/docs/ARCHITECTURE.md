# Architecture Documentation

## 🏗️ System Overview

The Django CMS is built using a modular, scalable architecture that separates concerns and allows for easy extension.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Bootstrap 5   │  │  JavaScript  │  │  Custom CSS    │  │
│  │   Templates    │  │  Components  │  │    Styles      │  │
│  └────────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django Application                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                      Views Layer                      │  │
│  │  • Class-based views  • Template rendering           │  │
│  │  • URL routing        • Context processors           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Business Logic                     │  │
│  │  • Models (Pages, Sections, Blocks)                  │  │
│  │  • Signals (Cache invalidation)                      │  │
│  │  • Template tags (Content rendering)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                     REST API Layer                    │  │
│  │  • Serializers  • ViewSets  • Permissions            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │   PostgreSQL   │  │  File System │  │  Cache (Redis) │  │
│  │   (Database)   │  │   (Media)    │  │   (Optional)   │  │
│  └────────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Component Architecture

### 1. Models Layer

#### Core Models

**SiteConfiguration** (Singleton)
- Global site settings
- Branding (logo, colors, fonts)
- SEO defaults
- Social media links

**Page**
- Title, slug, meta data
- Published/draft status
- Homepage flag
- Relationships: has many Sections

**Section**
- Section type (hero, text, gallery, etc.)
- Styling (background, padding, colors)
- Visibility control
- Relationships: belongs to Page, has many ContentBlocks

**ContentBlock**
- Block type (rich text, image, video, etc.)
- Content fields (text, image, link)
- Configuration JSON
- Relationships: belongs to Section, has many GalleryImages (for gallery blocks)

**MenuItem**
- Navigation structure
- Link types (page, section, external)
- Parent/child hierarchy
- Relationships: self-referential (parent/children)

**Media**
- File storage
- Metadata (alt text, tags)
- Auto-detected type
- File size and dimensions

### 2. Admin Layer

#### Features
- Inline editing (Sections within Pages, Blocks within Sections)
- Sortable lists with drag-and-drop
- Rich text editor (CKEditor)
- Image previews and thumbnails
- Import/Export capabilities
- Custom admin actions

#### Admin Classes
```python
PageAdmin
├── Inlines: SectionInline
└── Features: Sortable, Preview links

SectionAdmin
├── Inlines: ContentBlockInline
└── Features: Sortable, Type filtering

ContentBlockAdmin
├── Inlines: GalleryImageInline
└── Features: Type filtering, Media preview
```

### 3. Views Layer

#### Class-Based Views

**HomePageView** (DetailView)
- Fetches homepage (is_home=True)
- Loads all visible sections with blocks
- Template caching (15 minutes)

**PageDetailView** (DetailView)
- Fetches page by slug
- Loads sections and blocks (prefetch_related for performance)
- Template caching

**MediaLibraryView** (ListView)
- Paginated media listing
- Filtering by type
- Search functionality

### 4. Template System

#### Template Hierarchy
```
base.html (Layout foundation)
├── includes/navigation.html
├── page.html (Content renderer)
│   └── includes/section.html (Section renderer)
│       └── Template tags render content blocks
└── includes/footer.html
```

#### Template Tags
- `render_content_block`: Renders block based on type
- `render_section`: Renders complete section
- `section_style`: Generates inline CSS
- `block_style`: Generates block CSS

### 5. API Layer

#### REST API Architecture
```
API Endpoints
├── /api/pages/              (PageViewSet)
├── /api/sections/           (SectionViewSet)
├── /api/content-blocks/     (ContentBlockViewSet)
├── /api/menu-items/         (MenuItemViewSet)
├── /api/media/              (MediaViewSet)
└── /api/site-config/        (SiteConfigurationViewSet)
```

#### Serializers Hierarchy
- List serializers (minimal data)
- Detail serializers (nested relationships)
- Nested serializers for related objects

## 🔄 Data Flow

### Page Rendering Flow

```
1. User requests page
   │
   ▼
2. URL router matches slug
   │
   ▼
3. PageDetailView.get_object()
   │
   ▼
4. Query database (with prefetch_related)
   │
   ▼
5. Context processor adds site config & menu
   │
   ▼
6. Render template
   │
   ▼
7. Loop through sections
   │
   ▼
8. For each section, loop through blocks
   │
   ▼
9. Template tag renders each block
   │
   ▼
10. Return HTML response
```

### Admin Content Creation Flow

```
1. Admin creates Page
   │
   ▼
2. Add Section (inline)
   ├── Auto-generate anchor ID from title
   └── Set default padding values
   │
   ▼
3. Add ContentBlock (inline)
   ├── Choose block type
   └── Fill type-specific fields
   │
   ▼
4. Save Page
   ├── Trigger post_save signal
   ├── Clear cache
   └── Return to admin
```

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────────┐
│  SiteConfiguration  │
│  (Singleton)        │
└─────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐
│       Page          │─────┬──<│      Section        │
│  • id               │     │   │  • id               │
│  • title            │     │   │  • section_type     │
│  • slug (unique)    │     │   │  • title            │
│  • status           │     │   │  • anchor_id        │
│  • is_home          │     │   │  • is_visible       │
│  • order            │     │   │  • config (JSON)    │
└─────────────────────┘     │   │  • order            │
                            │   └─────────────────────┘
                            │              │
                            │              │ 1:N
                            │              ▼
                            │   ┌─────────────────────┐
                            │   │   ContentBlock      │
                            │   │  • id               │
                            │   │  • block_type       │
                            │   │  • content          │
                            │   │  • image            │
                            │   │  • config (JSON)    │
                            │   │  • order            │
                            │   └─────────────────────┘
                            │              │
                            │              │ 1:N
                            │              ▼
                            │   ┌─────────────────────┐
                            │   │   GalleryImage      │
                            │   │  • id               │
                            │   │  • image            │
                            │   │  • alt_text         │
                            │   │  • order            │
                            │   └─────────────────────┘
                            │
                            │   ┌─────────────────────┐
                            └──<│     MenuItem        │
                                │  • id               │
                                │  • label            │
                                │  • link_type        │
                                │  • page (FK)        │
                                │  • section (FK)     │
                                │  • parent (FK self) │
                                └─────────────────────┘

┌─────────────────────┐
│       Media         │
│  • id               │
│  • title            │
│  • file             │
│  • media_type       │
│  • file_size        │
│  • width/height     │
└─────────────────────┘
```

## 🎯 Design Patterns

### 1. Template Method Pattern
Used in block rendering - base logic in template tag, specific rendering per block type.

### 2. Strategy Pattern
Different section types have different rendering strategies.

### 3. Observer Pattern
Django signals for cache invalidation on model changes.

### 4. Singleton Pattern
SiteConfiguration ensures only one instance exists.

### 5. Repository Pattern
API ViewSets abstract data access logic.

## 🔌 Extension Points

### Adding New Section Types

1. Add choice to `Section.SECTION_TYPES`
2. Update `includes/section.html` template
3. Add specific rendering logic

### Adding New Block Types

1. Add choice to `ContentBlock.BLOCK_TYPES`
2. Update `render_content_block` template tag
3. Add admin fields if needed

### Adding New API Endpoints

1. Create ViewSet in `api/views.py`
2. Create Serializer in `api/serializers.py`
3. Register router in `api/urls.py`

## ⚡ Performance Optimizations

### Database Level
- Indexes on slug, status, is_visible fields
- prefetch_related for nested queries
- select_related for foreign keys

### Application Level
- Template fragment caching
- Cached template loader (production)
- Signal-based cache invalidation

### Frontend Level
- Lazy loading images
- Minified CSS/JS (WhiteNoise compression)
- CDN for static files (optional)

## 🔐 Security Measures

### Input Validation
- Django forms validation
- Model field constraints
- Admin permissions

### Output Encoding
- Django template auto-escaping
- mark_safe only where needed
- CSRF protection enabled

### Authentication
- Django admin authentication
- API read-only by default
- Staff-only admin access

## 📊 Monitoring Points

### Application Metrics
- Page load times
- Database query counts
- Cache hit rates
- API response times

### System Metrics
- CPU/Memory usage
- Disk space (media files)
- Database connections
- Request rate

## 🚀 Scalability Considerations

### Horizontal Scaling
- Stateless application design
- External file storage (S3)
- Centralized cache (Redis)
- Load balancer friendly

### Vertical Scaling
- Optimized queries
- Connection pooling
- Efficient caching
- Background task processing (Celery - future)

## 🔮 Future Architecture Enhancements

- [ ] Celery for async tasks
- [ ] ElasticSearch for advanced search
- [ ] GraphQL API endpoint
- [ ] Multi-language support
- [ ] Versioning for content
- [ ] Workflow/approval system
- [ ] Analytics dashboard
- [ ] A/B testing framework
