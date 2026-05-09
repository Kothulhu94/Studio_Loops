import os
import json
import time

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class PlaywrightResearch:
    def __init__(self, config=None):
        self.config = config or {}
        self.available = PLAYWRIGHT_AVAILABLE
        self._browser_available = None
        self.browser_profile_dir = os.path.abspath(".agent/logs/research/browser_profile/")
        
    def is_available(self):
        if not self.available:
            return False
        if self._browser_available is not None:
            return self._browser_available
            
        try:
            with sync_playwright() as p:
                # Just probe if it can launch
                browser = p.chromium.launch(headless=True)
                browser.close()
                self._browser_available = True
        except Exception:
            self._browser_available = False
        return self._browser_available

    def get_install_hint(self):
        if not self.available:
            return r"Run: \PortablePython\python.exe -m pip install playwright"
        if not self._browser_available:
            return r"Run: \PortablePython\python.exe -m playwright install chromium"
        return ""

    def run_search(self, query, search_url_template):
        if not self.available:
            return {"error": "Playwright not installed."}
            
        search_url = search_url_template.format(query=query.replace(" ", "+"))
        
        with sync_playwright() as p:
            # Use persistent context to help with bot detection
            context = p.chromium.launch_persistent_context(
                self.browser_profile_dir,
                headless=self.config.get("headless", False),
                user_agent=self.config.get("user_agent", "Mozilla/5.0 StudioLoopLocalGemmaResearch/1.0")
            )
            page = context.new_page()
            page.on("console", lambda msg: print(f"BROWSER: {msg.text}"))
            
            try:
                print(f"Navigating to {search_url}...")
                page.goto(search_url, timeout=30000)
                try:
                    # Wait for network idle
                    page.wait_for_load_state("networkidle", timeout=15000)
                except:
                    pass
                
                # Small sleep for final rendering
                time.sleep(3)
                page.screenshot(path="debug_search.png")
                
                # Aggressively extract all links from all Shadow DOMs
                extracted_links = []
                try:
                    extracted_links = page.evaluate("""
                        (function() {
                            function getAllAnchors(root) {
                                let results = [];
                                const anchors = root.querySelectorAll('a');
                                for (const a of anchors) {
                                    if (a.href) results.push({url: a.href, title: a.innerText});
                                }
                                const all = root.querySelectorAll('*');
                                for (const el of all) {
                                    if (el.shadowRoot) {
                                        results = results.concat(getAllAnchors(el.shadowRoot));
                                    }
                                }
                                return results;
                            }
                            return getAllAnchors(document);
                        })();
                    """)
                except:
                    pass

                # Detect CAPTCHA/Login
                content = page.content()
                if "captcha" in content.lower() or "verification" in content.lower():
                    # Check if it's actually blocked or just a false positive in a large page
                    if len(content) < 5000: 
                        return {"error": "Search blocked by CAPTCHA."}
                
                return {"html": content, "url": page.url, "links": extracted_links}
            except Exception as e:
                return {"error": str(e)}
            finally:
                context.close()

    def fetch_page(self, url):
        if not self.available:
            return {"error": "Playwright not installed."}
            
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.config.get("headless", False))
            page = browser.new_page(user_agent=self.config.get("user_agent"))
            
            try:
                page.goto(url, timeout=30000)
                try:
                    page.wait_for_load_state("load", timeout=10000)
                except:
                    pass
                return {"html": page.content(), "url": page.url}

            except Exception as e:
                return {"error": str(e)}
            finally:
                browser.close()
