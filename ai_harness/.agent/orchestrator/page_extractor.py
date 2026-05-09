import hashlib
import os
import re
from datetime import datetime


MOJIBAKE_MARKERS = [
    "\ufffd",
    "\u00c3",
    "\u00c2",
    "\u00e2\u20ac",
    "\u00e2\u20ac\u2122",
    "\u00e2\u20ac\u0153",
    "\u00e2\u20ac\u009d",
    "\u00e2\u20ac\u201d",
    "\u00e2\u20ac\u201c",
    "\u00f0\u0178",
    "\u00d8",
    "\u00d9",
    "\u00d0",
    "\u00d1",
]


class PageExtractor:
    def __init__(self, config=None, base_path=None):
        self.config = config or {}
        self.base_path = base_path or os.getcwd()
        self.cache_dir = os.path.join(
            self.base_path,
            self.config.get("cache_dir", ".agent/logs/research/cache/pages"),
        )

    def extract(self, url, html_content):
        import html

        html_content = html.unescape(html_content)
        content = re.sub(
            r"<(script|style|nav|footer)[^>]*>.*?</\1>",
            "",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Unknown Title"
        title = html.unescape(title)

        headings = re.findall(r"<(h[1-6])>(.*?)</\1>", content, re.IGNORECASE)
        heading_text = "\n".join([f"{h}: {html.unescape(t)}" for h, t in headings])

        text = re.sub("<[^<]+?>", "", content)
        text = re.sub(r"\s+", " ", text).strip()

        bad_marker_count = sum(text.count(marker) for marker in MOJIBAKE_MARKERS)
        non_ascii_count = sum(1 for char in text if ord(char) > 127)
        non_ascii_ratio = non_ascii_count / max(len(text), 1)
        is_mojibake = bad_marker_count > 0 or non_ascii_ratio > 0.25

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

        os.makedirs(self.cache_dir, exist_ok=True)
        file_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f"{file_hash}.md")
        with open(cache_path, "w", encoding="utf-8") as handle:
            handle.write(md_content)

        return {
            "title": title,
            "url": url,
            "retrieved_at": retrieved,
            "cache_path": cache_path,
            "excerpt": text[:2000],
            "status": "failed" if is_mojibake else "fetched",
            "notes": "mojibake / encoding corruption" if is_mojibake else "",
        }
