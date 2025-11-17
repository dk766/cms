# API Documentation

## Overview

The CMS provides a comprehensive REST API built with Django REST Framework. All endpoints return JSON and support filtering, searching, and pagination.

**Base URL**: `http://localhost:8000/api/`

## Authentication

By default, the API allows read-only access without authentication. For write operations (future enhancement), authentication will be required.

## Endpoints

### Pages

#### List All Pages
```http
GET /api/pages/
```

**Query Parameters**:
- `is_home` (boolean): Filter homepage
- `status` (string): Filter by status (published/draft)
- `search` (string): Search in title and meta description
- `ordering` (string): Sort by field (e.g., `-created_at`)

**Response**:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Home",
      "slug": "home",
      "meta_title": "Welcome to Our Site",
      "meta_description": "...",
      "status": "published",
      "status_display": "Published",
      "is_home": true,
      "order": 0,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z",
      "url": "/"
    }
  ]
}
```

#### Get Single Page
```http
GET /api/pages/{slug}/
```

**Response includes**:
- Page details
- All sections (ordered)
- All content blocks (ordered)
- Gallery images

```json
{
  "id": 1,
  "title": "Home",
  "slug": "home",
  "sections": [
    {
      "id": 1,
      "section_type": "hero",
      "section_type_display": "Hero Section",
      "title": "Welcome Section",
      "anchor_id": "welcome",
      "is_visible": true,
      "background_color": "#ffffff",
      "content_blocks": [
        {
          "id": 1,
          "block_type": "rich_text",
          "block_type_display": "Rich Text",
          "title": null,
          "content": "<h1>Welcome</h1>",
          "image": null,
          "link_url": null,
          "order": 0
        }
      ]
    }
  ]
}
```

#### Get Homepage
```http
GET /api/pages/homepage/
```

Returns the designated homepage or first published page.

### Sections

#### List Sections
```http
GET /api/sections/
```

**Query Parameters**:
- `page` (integer): Filter by page ID
- `section_type` (string): Filter by type
- `is_visible` (boolean): Filter visibility
- `ordering` (string): Sort by field

**Response**:
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "section_type": "hero",
      "section_type_display": "Hero Section",
      "title": "Welcome",
      "anchor_id": "welcome",
      "is_visible": true,
      "background_color": "#f8f9fa",
      "background_image": null,
      "text_color": "#212529",
      "padding_top": 60,
      "padding_bottom": 60,
      "css_class": "",
      "config": {},
      "order": 0,
      "content_blocks": [...]
    }
  ]
}
```

### Content Blocks

#### List Content Blocks
```http
GET /api/content-blocks/
```

**Query Parameters**:
- `section` (integer): Filter by section ID
- `block_type` (string): Filter by type
- `ordering` (string): Sort by field

### Menu Items

#### Get Navigation Menu
```http
GET /api/menu-items/
```

Returns top-level menu items with nested children.

**Response**:
```json
[
  {
    "id": 1,
    "label": "Home",
    "link_type": "page",
    "link_type_display": "Internal Page",
    "url": "/",
    "is_visible": true,
    "order": 0,
    "children": []
  },
  {
    "id": 2,
    "label": "Services",
    "link_type": "page",
    "url": "/services/",
    "children": [
      {
        "id": 3,
        "label": "Web Design",
        "url": "/services/#web-design",
        "children": []
      }
    ]
  }
]
```

### Media Library

#### List Media Files
```http
GET /api/media/
```

**Query Parameters**:
- `media_type` (string): Filter by type (image/document/video/other)
- `search` (string): Search in title, alt text, and tags
- `ordering` (string): Sort by field

**Response**:
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "title": "Hero Image",
      "file": "/media/uploads/2024/01/hero.jpg",
      "file_url": "http://localhost:8000/media/uploads/2024/01/hero.jpg",
      "media_type": "image",
      "media_type_display": "Image",
      "alt_text": "Homepage hero image",
      "caption": "Beautiful landscape",
      "file_size": 245678,
      "width": 1920,
      "height": 1080,
      "tags": "hero, landscape, homepage",
      "uploaded_at": "2024-01-01T00:00:00Z",
      "thumbnail_url": "http://localhost:8000/media/uploads/2024/01/hero.jpg"
    }
  ]
}
```

### Site Configuration

#### Get Site Config
```http
GET /api/site-config/current/
```

Returns current site configuration (colors, branding, etc.).

**Response**:
```json
{
  "id": 1,
  "site_name": "My Website",
  "logo": "/media/branding/logo.png",
  "favicon": "/media/branding/favicon.ico",
  "primary_color": "#007bff",
  "secondary_color": "#6c757d",
  "text_color": "#212529",
  "background_color": "#ffffff",
  "font_family": "Arial, sans-serif",
  "base_font_size": 16,
  "footer_text": "<p>© 2024 My Website</p>",
  "footer_background_color": "#343a40",
  "footer_text_color": "#ffffff",
  "facebook_url": "https://facebook.com/...",
  "twitter_url": null,
  "linkedin_url": null,
  "instagram_url": null
}
```

## Filtering Examples

### Get All Hero Sections
```http
GET /api/sections/?section_type=hero
```

### Search Pages
```http
GET /api/pages/?search=about
```

### Get Images Only
```http
GET /api/media/?media_type=image
```

### Sort by Date
```http
GET /api/pages/?ordering=-created_at
```

## Pagination

All list endpoints support pagination:

```http
GET /api/pages/?page=2
```

Default page size: 20 items

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Update `settings.py` to add your domain.

## Rate Limiting

No rate limiting is currently implemented. Consider adding for production.

## Headless CMS Usage

### React Example

```javascript
// Fetch homepage
fetch('http://localhost:8000/api/pages/homepage/')
  .then(res => res.json())
  .then(data => {
    console.log(data.sections);
    // Render sections and blocks
  });
```

### Vue Example

```javascript
// In your component
export default {
  data() {
    return {
      page: null
    }
  },
  mounted() {
    fetch('http://localhost:8000/api/pages/home/')
      .then(res => res.json())
      .then(data => {
        this.page = data;
      });
  }
}
```

### Next.js Example

```javascript
// In getStaticProps
export async function getStaticProps() {
  const res = await fetch('http://localhost:8000/api/pages/homepage/');
  const page = await res.json();

  return {
    props: { page },
    revalidate: 60 // Revalidate every 60 seconds
  };
}
```

## Best Practices

1. **Cache responses** when possible
2. **Use specific endpoints** rather than fetching all data
3. **Filter on server side** using query parameters
4. **Handle errors gracefully**
5. **Respect rate limits** (when implemented)
6. **Use HTTPS** in production

## Future Enhancements

- [ ] Write endpoints (POST, PUT, DELETE)
- [ ] Authentication with tokens
- [ ] Rate limiting
- [ ] Webhooks for content changes
- [ ] GraphQL endpoint
- [ ] API versioning
