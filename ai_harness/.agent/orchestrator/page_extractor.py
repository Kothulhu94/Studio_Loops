import re
import os
import hashlib
from datetime import datetime

class PageExtractor:
    def __init__(self, config=None):
        self.config = config or {}
        self.cache_dir = self.config.get("cache_dir", ".agent/logs/research/cache/pages")

    def extract(self, url, html_content):
        import html
        # 0. Normalize text
        html_content = html.unescape(html_content)

        # 1. Clean HTML
        # Remove scripts, styles, nav, footer
        content = re.sub(r'<(script|style|nav|footer)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Unknown Title"
        title = html.unescape(title)
        
        # Extract headings
        headings = re.findall(r'<(h[1-6])>(.*?)</\1>', content, re.IGNORECASE)
        heading_text = "\n".join([f"{h}: {html.unescape(t)}" for h, t in headings])
        
        # Extract visible text
        text = re.sub('<[^<]+?>', '', content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Mojibake detection
        bad_markers = [
            "Ã", "Â", "â€", "â€™", "â€œ", "â€",
            "ðŸ", "Ø", "Ù", "Ð", "Ñ", "É™", "Ä°"
        ]
        bad_marker_count = sum(text.count(m) for m in bad_markers)
        bad_ratio = bad_marker_count / max(len(text), 1)
        
        # Non-ASCII ratio (penalize if high for English query context)
        non_ascii_count = sum(1 for c in text if ord(c) > 127)
        non_ascii_ratio = non_ascii_count / max(len(text), 1)
        
        is_mojibake = bad_ratio > 0.05 or non_ascii_ratio > 0.25
        
        # 2. Format as Markdown
        retrieved = datetime.now().isoformat()
        md_content = f"""# Extracted Page

## Title
{title}

## URL
{url}

## Retrieved
{retrieved}

## Headings
{heading_text}

## Visible Text
{text[:10000]} # Truncated for display

## Notes
Extracted via Studio Loop Local PageExtractor
{"[WARNING] Mojibake detected!" if is_mojibake else ""}
"""
        
        # 3. Save to cache
        os.makedirs(self.cache_dir, exist_ok=True)
        file_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f"{file_hash}.md")
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return {
            "title": title,
            "url": url,
            "retrieved_at": retrieved,
            "cache_path": cache_path,
            "excerpt": text[:2000],
            "status": "failed" if is_mojibake else "fetched",
            "notes": "mojibake / encoding corruption" if is_mojibake else ""
        }
