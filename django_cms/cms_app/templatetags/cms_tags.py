"""
Custom template tags for CMS.
"""
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary."""
    return dictionary.get(key)


@register.simple_tag
def render_content_block(block):
    """
    Render a content block based on its type.
    Returns HTML for the block.
    """
    if block.block_type == 'rich_text':
        return mark_safe(f'<div class="content-block-text">{block.content or ""}</div>')

    elif block.block_type == 'heading':
        level = block.config.get('heading_level', 2)
        return mark_safe(f'<h{level} class="content-block-heading">{block.title or ""}</h{level}>')

    elif block.block_type == 'image':
        if block.image:
            alt = block.image_alt or block.title or ''
            return mark_safe(f'''
                <div class="content-block-image text-center">
                    <img src="{block.image.url}" alt="{alt}" class="img-fluid rounded" />
                    {f'<p class="mt-2 text-muted"><small>{block.title}</small></p>' if block.title else ''}
                </div>
            ''')

    elif block.block_type == 'gallery':
        images = block.gallery_images.all()
        if images:
            html = '<div class="content-block-gallery row g-3">'
            for img in images:
                html += f'''
                    <div class="col-md-4 col-sm-6">
                        <div class="gallery-item">
                            <img src="{img.image.url}" alt="{img.alt_text or ''}" class="img-fluid rounded" />
                            {f'<p class="mt-2 text-center"><small>{img.caption}</small></p>' if img.caption else ''}
                        </div>
                    </div>
                '''
            html += '</div>'
            return mark_safe(html)

    elif block.block_type == 'video':
        video_url = block.link_url or ''
        if 'youtube.com' in video_url or 'youtu.be' in video_url:
            # Extract YouTube video ID
            if 'youtu.be' in video_url:
                video_id = video_url.split('/')[-1]
            else:
                video_id = video_url.split('v=')[1].split('&')[0] if 'v=' in video_url else ''

            if video_id:
                return mark_safe(f'''
                    <div class="content-block-video ratio ratio-16x9">
                        <iframe src="https://www.youtube.com/embed/{video_id}"
                                allowfullscreen
                                class="rounded"></iframe>
                    </div>
                ''')

        elif 'vimeo.com' in video_url:
            video_id = video_url.split('/')[-1]
            return mark_safe(f'''
                <div class="content-block-video ratio ratio-16x9">
                    <iframe src="https://player.vimeo.com/video/{video_id}"
                            allowfullscreen
                            class="rounded"></iframe>
                </div>
            ''')

    elif block.block_type == 'button':
        if block.link_url and block.link_text:
            return mark_safe(f'''
                <div class="content-block-button text-center">
                    <a href="{block.link_url}"
                       class="btn btn-{block.button_style} btn-lg"
                       target="{block.link_target}">
                        {block.link_text}
                    </a>
                </div>
            ''')

    elif block.block_type == 'icon_text':
        icon = block.config.get('icon', 'bi-star')
        return mark_safe(f'''
            <div class="content-block-icon-text text-center">
                <i class="bi {icon} fs-1 text-primary mb-3"></i>
                {f'<h4>{block.title}</h4>' if block.title else ''}
                {f'<div>{block.content}</div>' if block.content else ''}
            </div>
        ''')

    elif block.block_type == 'code':
        language = block.config.get('language', 'python')
        return mark_safe(f'''
            <div class="content-block-code">
                <pre><code class="language-{language}">{block.html_content or block.content or ''}</code></pre>
            </div>
        ''')

    elif block.block_type == 'spacer':
        height = block.config.get('height', 40)
        return mark_safe(f'<div class="content-block-spacer" style="height: {height}px;"></div>')

    elif block.block_type == 'divider':
        return mark_safe('<hr class="content-block-divider my-4" />')

    elif block.block_type == 'html':
        return mark_safe(f'<div class="content-block-html">{block.html_content or ""}</div>')

    return mark_safe(f'<div class="content-block">Content block: {block.block_type}</div>')


@register.inclusion_tag('cms_app/includes/section.html')
def render_section(section):
    """
    Render a complete section with all its content blocks.
    """
    return {
        'section': section,
        'blocks': section.content_blocks.all().order_by('order')
    }


@register.filter
def parse_json(value):
    """Parse JSON string to Python object."""
    try:
        return json.loads(value) if isinstance(value, str) else value
    except (json.JSONDecodeError, TypeError):
        return {}


@register.simple_tag
def section_style(section):
    """
    Generate inline CSS for section styling.
    """
    styles = []

    if section.background_color:
        styles.append(f'background-color: {section.background_color}')

    if section.background_image:
        styles.append(f'background-image: url({section.background_image.url})')
        styles.append('background-size: cover')
        styles.append('background-position: center')

    if section.text_color:
        styles.append(f'color: {section.text_color}')

    if section.padding_top:
        styles.append(f'padding-top: {section.padding_top}px')

    if section.padding_bottom:
        styles.append(f'padding-bottom: {section.padding_bottom}px')

    return mark_safe('; '.join(styles))


@register.simple_tag
def block_style(block):
    """
    Generate inline CSS for content block styling.
    """
    styles = []

    if block.background_color:
        styles.append(f'background-color: {block.background_color}')

    if block.text_color:
        styles.append(f'color: {block.text_color}')

    return mark_safe('; '.join(styles))


@register.filter
def youtube_embed_url(url):
    """Convert YouTube URL to embed URL."""
    if not url:
        return ''

    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
    elif 'youtube.com' in url and 'v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
    else:
        return url

    return f'https://www.youtube.com/embed/{video_id}'


@register.filter
def vimeo_embed_url(url):
    """Convert Vimeo URL to embed URL."""
    if not url:
        return ''

    video_id = url.split('/')[-1]
    return f'https://player.vimeo.com/video/{video_id}'
