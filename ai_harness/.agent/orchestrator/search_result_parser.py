import re
import urllib.parse
import html

class SearchResultParser:
    def __init__(self, engine="duckduckgo_lite"):
        self.engine = engine

    def parse_links(self, html_content):
        """Parses result links from search engine HTML content."""
        links = []
        
        # Decode HTML entities first
        html_content = html.unescape(html_content)


        
        if self.engine == "duckduckgo_lite":
            # 1. Match typical result links
            # DuckDuckGo Lite result links often have class 'result-link' or similar
            # Or they are inside 'result__a' in some versions
            
            # Pattern for direct links
            direct_pattern = r'<a[^>]+href=["\'](http[s]?://[^"\']+)["\'][^>]*>(.*?)</a>'
            matches = re.findall(direct_pattern, html_content)
            
            for url, title in matches:
                # Filter out internal links and ads
                if any(domain in url for domain in ["duckduckgo.com", "google.com", "bing.com", "yandex.com"]):
                    # Check if it's a redirect link: /l/?uddg=...
                    if "/l/?uddg=" in url or "//duckduckgo.com/l/?uddg=" in url:
                        parsed = urllib.parse.urlparse(url)
                        params = urllib.parse.parse_qs(parsed.query)
                        if 'uddg' in params:
                            url = params['uddg'][0]
                        else:
                            continue
                    else:
                        continue
                
                clean_title = self._clean_text(title)
                if clean_title and url:
                    links.append({"url": url, "title": clean_title})

            # 2. Match relative /l/?uddg links that might have been missed
            redirect_pattern = r'href=["\'](/[l]/\?uddg=[^"\']+)["\'][^>]*>(.*?)</a>'
            matches = re.findall(redirect_pattern, html_content)
            for path, title in matches:
                params = urllib.parse.parse_qs(urllib.parse.urlparse(path).query)
                if 'uddg' in params:
                    url = params['uddg'][0]
                    clean_title = self._clean_text(title)
                    if clean_title and url:
                        links.append({"url": url, "title": clean_title})
        else:
            # Generic parser for other engines (Bing, Google, etc.)
            direct_pattern = r'<a[^>]+href=["\'](http[s]?://[^"\']+|/[^"\']+)["\'][^>]*>(.*?)</a>'
            matches = re.findall(direct_pattern, html_content)
            
            for url, title in matches:
                # Handle relative links
                if url.startswith("/"):
                    if self.engine == "mdn":
                        url = "https://developer.mozilla.org" + url
                    else:
                        url = "https://www.bing.com" + url

                # MDN specific filtering
                if self.engine == "mdn":
                    # Require docs path
                    if "developer.mozilla.org/en-US/docs/" not in url:
                        continue
                    # Reject curriculum, plus, play, blog
                    if any(bad in url for bad in ["/curriculum/", "/plus", "/play", "/blog", "github.com/mdn", "scrimba.com"]):
                        continue
                    # Reject very generic landing pages
                    if any(url.endswith(gen) for gen in ["/docs/Web/HTML", "/docs/Web/JavaScript", "/docs/Web/API", "/docs/Web"]):
                        continue

                # Filter out search engine internal links and ads
                if any(domain in url for domain in ["bing.com", "microsoft.com", "google.com", "duckduckgo.com", "yandex.com"]):
                    if not url.startswith("http") or any(domain in url for domain in ["bing.com", "microsoft.com", "google.com"]):
                        continue
                
                if "/search?" in url or "go.microsoft.com" in url:
                    continue

                clean_title = self._clean_text(title)
                if clean_title and len(clean_title) > 2 and url.startswith("http"):
                    links.append({"url": url, "title": clean_title})



        # Deduplicate
        seen_keys = set()
        unique_links = []
        for l in links:
            try:
                url = l["url"]
                domain = urllib.parse.urlparse(url).netloc
                
                if self.engine == "mdn":
                    # Dedupe by normalized URL path
                    dedupe_key = url.split("?")[0].split("#")[0].rstrip("/")
                else:
                    dedupe_key = domain
                    
                if dedupe_key not in seen_keys and domain:
                    unique_links.append(l)
                    seen_keys.add(dedupe_key)
            except:
                continue
                
        return unique_links[:10]

    def _clean_text(self, text):
        # Remove HTML tags
        clean = re.sub('<[^<]+?>', '', text)
        # Remove extra whitespace
        clean = " ".join(clean.split())
        return clean.strip()
