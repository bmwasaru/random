import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import markdownify
from urllib.parse import urlparse

NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

def download_image(url, output_dir="assets/images"):
    if not url.startswith('http'):
        return url
        
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return url
        
    local_path = os.path.join(output_dir, filename)
    
    # The relative path Jekyll will use in the compiled HTML
    jekyll_path = f"/assets/images/{filename}"
    
    if not os.path.exists(local_path):
        try:
            # Mask as a standard browser to prevent WordPress security plugins from blocking the download
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, stream=True, headers=headers, timeout=15)
            
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"  -> Downloaded: {filename}")
            else:
                print(f"  -> Failed (HTTP {response.status_code}): {url}")
        except Exception as e:
            print(f"  -> Error downloading {url}: {e}")
            return url
            
    return jekyll_path

def convert_wp_to_jekyll(xml_file, posts_dir="_posts", img_dir="assets/images"):
    # Build Jekyll's exact required directory structure
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for item in root.findall('.//item'):
        post_type = item.find('wp:post_type', NAMESPACES)
        status = item.find('wp:status', NAMESPACES)
        
        if post_type is None or post_type.text != 'post':
            continue
        if status is None or status.text != 'publish':
            continue

        title = item.find('title').text or "Untitled"
        slug = item.find('wp:post_name', NAMESPACES).text
        if not slug:
            slug = title.lower().replace(" ", "-")
            
        date_str = item.find('wp:post_date', NAMESPACES).text
        content_html = item.find('content:encoded', NAMESPACES).text or ""

        # Parse HTML to find, download, and relink images before converting to Markdown
        soup = BeautifulSoup(content_html, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                new_src = download_image(src, img_dir)
                img['src'] = new_src
                
        content_md = markdownify.markdownify(str(soup), heading_style="ATX")

        tags = []
        categories = []
        for cat in item.findall('category'):
            domain = cat.get('domain')
            if domain == 'post_tag':
                tags.append(cat.text)
            elif domain == 'category':
                categories.append(cat.text)

        safe_title = title.replace('"', '\\"')
        
        # Build Jekyll-specific YAML Frontmatter
        yaml = "---\n"
        yaml += f'layout: post\n'
        yaml += f'title: "{safe_title}"\n'
        yaml += f'date: {date_str}\n'
        
        if categories:
            yaml += f"categories: [{', '.join([f'\"{c}\"' for c in categories])}]\n"
        if tags:
            yaml += f"tags: [{', '.join([f'\"{t}\"' for t in tags])}]\n"
            
        yaml += "---\n\n"

        safe_date = date_str[:10]
        filename = f"{safe_date}-{slug}.md"
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml + content_md)
            
        print(f"Exported: {filename}")

if __name__ == "__main__":
    # Point this to your WordPress WXR XML export
    convert_wp_to_jekyll("export.xml")
