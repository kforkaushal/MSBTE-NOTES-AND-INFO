"""
Update all HTML files in Branches/ to reference their corresponding 1200x630 PNG thumbnail
in hero <img> banners, Open Graph (<meta property="og:image">), Twitter cards, and JSON-LD schema.
"""

import os
import glob
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCHES_DIR = os.path.join(BASE_DIR, 'Branches')
MEDIA_DIR = os.path.join(BRANCHES_DIR, 'media')
SITE_URL = "https://msbtenotes-info.netlify.app"

def update_branch_pages():
    html_files = glob.glob(os.path.join(BRANCHES_DIR, '*.html'))
    print(f"Total HTML files to inspect in {BRANCHES_DIR}: {len(html_files)}")
    
    updated_count = 0
    
    for fpath in html_files:
        base = os.path.basename(fpath)
        stem = base[:-5] # remove .html
        
        # Check if matching png exists in Branches/media/
        png_name = stem + '.png'
        png_path = os.path.join(MEDIA_DIR, png_name)
        
        target_stem = stem
        if not os.path.exists(png_path):
            # Check for slight variations (e.g. 3316326 vs 316326)
            alt_stem = stem.replace('3316326', '316326') if '3316326' in stem else None
            if alt_stem and os.path.exists(os.path.join(MEDIA_DIR, alt_stem + '.png')):
                target_stem = alt_stem
                png_name = alt_stem + '.png'
            else:
                # If still not found, check if .svg exists
                if not os.path.exists(os.path.join(MEDIA_DIR, stem + '.svg')):
                    # No media file found for this html page
                    continue
        
        png_url = f"{SITE_URL}/Branches/media/{png_name}"
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Update Hero Image tag (replace .svg with .png if pointing to media/)
        content = re.sub(
            r'(<img\s+[^>]*src=["\'])media/([^"\']+)\.(svg|png)(["\'])',
            rf'\1media/{png_name}\4',
            content,
            count=1
        )
        
        # Also check for src="/Branches/media/..."
        content = re.sub(
            r'(<img\s+[^>]*src=["\'])(/Branches/media/)([^"\']+)\.(svg|png)(["\'])',
            rf'\1\2{png_name}\5',
            content,
            count=1
        )
        
        # 2. Update og:image
        # Check if og:image exists
        if 'property="og:image"' in content:
            content = re.sub(
                r'<meta\s+property=["\']og:image["\']\s+content=["\'][^"\']*["\']\s*/?>',
                f'<meta property="og:image" content="{png_url}" />',
                content
            )
        else:
            # Inject before </head>
            og_tag = f'    <meta property="og:image" content="{png_url}" />\n'
            content = content.replace('</head>', f'{og_tag}</head>', 1)
            
        # Update or add og:image:width and og:image:height and og:image:type
        if 'property="og:image:width"' in content:
            content = re.sub(
                r'<meta\s+property=["\']og:image:width["\']\s+content=["\'][^"\']*["\']\s*/?>',
                '<meta property="og:image:width" content="1200" />',
                content
            )
        else:
            content = re.sub(
                r'(<meta\s+property=["\']og:image["\'][^>]*>)',
                r'\1\n    <meta property="og:image:width" content="1200" />',
                content
            )
            
        if 'property="og:image:height"' in content:
            content = re.sub(
                r'<meta\s+property=["\']og:image:height["\']\s+content=["\'][^"\']*["\']\s*/?>',
                '<meta property="og:image:height" content="630" />',
                content
            )
        else:
            content = re.sub(
                r'(<meta\s+property=["\']og:image:width["\'][^>]*>)',
                r'\1\n    <meta property="og:image:height" content="630" />',
                content
            )
            
        if 'property="og:image:type"' in content:
            content = re.sub(
                r'<meta\s+property=["\']og:image:type["\']\s+content=["\'][^"\']*["\']\s*/?>',
                '<meta property="og:image:type" content="image/png" />',
                content
            )
        else:
            content = re.sub(
                r'(<meta\s+property=["\']og:image:height["\'][^>]*>)',
                r'\1\n    <meta property="og:image:type" content="image/png" />',
                content
            )
            
        # 3. Update twitter:image
        if 'name="twitter:image"' in content:
            content = re.sub(
                r'<meta\s+name=["\']twitter:image["\']\s+content=["\'][^"\']*["\']\s*/?>',
                f'<meta name="twitter:image" content="{png_url}" />',
                content
            )
        else:
            # Inject after og:image:type or before </head>
            tw_tag = f'    <meta name="twitter:image" content="{png_url}" />\n'
            content = content.replace('</head>', f'{tw_tag}</head>', 1)
            
        # 4. Update JSON-LD if it has image field
        # E.g. "image": "https://..."
        content = re.sub(
            r'("image":\s*")https://msbtenotes-info\.netlify\.app/[^"]*(")',
            rf'\1{png_url}\2',
            content
        )
        
        if content != original_content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            
    print(f"\n==========================================")
    print(f"SUCCESS: Updated {updated_count} HTML files in Branches/ with new PNG thumbnails & social meta tags.")
    print(f"==========================================")

if __name__ == '__main__':
    update_branch_pages()

