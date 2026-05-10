import os
import json
import sys
from urllib.parse import urlparse, urlunparse
import re

# Add the current directory to sys.path to allow absolute imports of sibling modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright_research import PlaywrightResearch
from search_result_parser import SearchResultParser
from page_extractor import PageExtractor

class BrowserResearch:
    def __init__(self, config=None, base_path=None):
        self.config = config or {}
        self.base_path = base_path or os.getcwd()
        self.research_config = self.config.get("web_research", {})
        self.playwright = PlaywrightResearch(self.research_config, self.base_path)
        self.parser = SearchResultParser(self.research_config.get("search_engine", "duckduckgo_lite"))
        self.extractor = PageExtractor(self.research_config, self.base_path)

    def _query_terms(self, query):
        stopwords = {
            "a", "an", "and", "api", "are", "as", "at", "best", "for", "how", "in",
            "is", "of", "on", "or", "the", "to", "use", "using", "with",
        }
        return [
            term for term in re.findall(r"[a-zA-Z][a-zA-Z0-9]+", query.lower())
            if len(term) >= 4 and term not in stopwords
        ]

    def _query_profile(self, query):
        q_lower = query.lower()
        if "canvas" in q_lower and "requestanimationframe" in q_lower:
            return "canvas_animation"
        ts_terms = [
            "typescript", "browser", "data model", "task queue", "queue",
            "worker task", "state management", "vitest",
        ]
        if any(term in q_lower for term in ts_terms):
            return "typescript_browser_architecture"
        return "generic_technical"

    def _query_variants(self, query):
        variants = [query]
        q_lower = query.lower()
        profile = self._query_profile(query)
        if profile == "canvas_animation":
            variants.extend([
                "Canvas API requestAnimationFrame MDN",
                "site:developer.mozilla.org/en-US/docs/Web/API Canvas requestAnimationFrame",
                "requestAnimationFrame Canvas MDN",
                "Canvas API basic animations MDN",
            ])
        elif profile == "typescript_browser_architecture":
            variants.extend([
                "TypeScript data model browser task queue Vitest",
                "TypeScript queue data structures browser unit testing Vitest",
                "JavaScript queue data structure browser state management",
            ])
        return list(dict.fromkeys(variants))

    def _canonical_candidates(self, query):
        profile = self._query_profile(query)
        candidates = []
        if profile == "canvas_animation":
            base = "https://developer.mozilla.org"
            paths = [
                "/en-US/docs/Web/API/Canvas_API",
                "/en-US/docs/Web/API/Window/requestAnimationFrame",
                "/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations",
                "/en-US/docs/Web/API/CanvasRenderingContext2D",
            ]
            candidates.extend({"url": base + path, "title": path.rsplit("/", 1)[-1]} for path in paths)
        elif profile == "typescript_browser_architecture":
            candidates.extend([
                {"url": "https://www.typescriptlang.org/docs/handbook/2/everyday-types.html", "title": "TypeScript Handbook - Everyday Types"},
                {"url": "https://www.typescriptlang.org/docs/handbook/2/objects.html", "title": "TypeScript Handbook - Object Types"},
                {"url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array", "title": "MDN JavaScript Array"},
                {"url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map", "title": "MDN JavaScript Map"},
                {"url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes", "title": "MDN JavaScript Classes"},
            ])
            q_lower = query.lower()
            if "test" in q_lower or "vitest" in q_lower:
                candidates.extend([
                    {"url": "https://vitest.dev/guide/", "title": "Vitest Guide"},
                    {"url": "https://vitest.dev/api/", "title": "Vitest API"},
                ])
        return candidates

    def _normalize_url(self, url):
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"), "", "", ""))

    def _topic_coverage(self, query, title, url, excerpt):
        haystack = " ".join([title or "", url or "", excerpt or ""]).lower()
        coverage = []
        checks = {
            "canvas": ["canvas api", "canvas_api", "canvasrenderingcontext2d", "htmlcanvas", "canvas "],
            "requestanimationframe": ["requestanimationframe"],
            "animation/rendering": ["animation", "animate", "render", "repaint", "frame"],
            "2d context": ["2d context", "canvasrenderingcontext2d", "getcontext", "2d graphics"],
            "basic animations": ["basic animations", "basic_animations"],
            "typescript": ["typescript", "strict types", "interface", "type alias", "generics"],
            "javascript data structures": ["array", "map", "set", "object", "queue", "fifo", "priority queue"],
            "queue/task scheduling": ["queue", "task", "scheduler", "priority", "dequeue", "enqueue", "worker"],
            "browser/runtime": ["browser", "web api", "webapi", "dom", "canvas", "requestanimationframe"],
            "testing/vitest": ["vitest", "unit test", "expect", "describe", "test"],
            "state/modeling": ["state", "model", "immutable", "reducer", "data model"],
        }
        for topic, needles in checks.items():
            if any(needle in haystack for needle in needles):
                coverage.append(topic)
        terms = self._query_terms(query)
        matched_terms = {term for term in terms if term in haystack}
        if len(matched_terms) >= 2:
            coverage.extend(f"query:{term}" for term in sorted(matched_terms))
        return coverage

    def _explicitly_requested_rejected_topic(self, query, keyword):
        q = query.lower()
        explicit = {
            "vrdisplay": ["vrdisplay", "webvr", "vr "],
            "xrsession": ["xrsession", "xr ", "webxr"],
            "webxr": ["webxr", "xr "],
            "deprecated": ["deprecated"],
            "experimental": ["experimental"],
            "non-standard": ["non-standard", "nonstandard"],
            "limited availability": ["limited availability"],
        }
        return any(term in q for term in explicit.get(keyword, [keyword]))

    def _rejection_reason(self, query, title, url, excerpt):
        haystack = " ".join([title or "", url or "", excerpt or ""]).lower()
        for keyword in [
            "vrdisplay", "xrsession", "webxr", "deprecated",
            "experimental", "non-standard", "limited availability",
        ]:
            if keyword in haystack and not self._explicitly_requested_rejected_topic(query, keyword):
                return f"rejected: contains {keyword}"
        return ""

    def _score_link(self, query, link):
        profile = self._query_profile(query)
        title_lower = link.get("title", "").lower()
        url_lower = link.get("url", "").lower()
        score = 0
        domain = urlparse(link.get("url", "")).netloc.lower()
        if "developer.mozilla.org" in domain:
            score += 40
        if "typescriptlang.org" in domain:
            score += 45 if profile == "typescript_browser_architecture" else 15
        if "vitest.dev" in domain:
            score += 45 if profile == "typescript_browser_architecture" else 10
        if "/en-us/docs/web/api/" in url_lower:
            score += 25
        if "/javascript/reference/global_objects/array" in url_lower or "/javascript/reference/global_objects/map" in url_lower:
            score += 35 if profile == "typescript_browser_architecture" else 10
        if "handbook" in url_lower and "typescript" in url_lower:
            score += 35
        if "vitest" in url_lower or "vitest" in title_lower:
            score += 35
        if "canvas_api/tutorial/basic_animations" in url_lower:
            score += 45
        if "window/requestanimationframe" in url_lower:
            score += 45
        if "canvas_api" in url_lower or "canvas api" in title_lower:
            score += 35
        if "canvasrenderingcontext2d" in url_lower or "canvasrenderingcontext2d" in title_lower:
            score += 30
        if "requestanimationframe" in url_lower or "requestanimationframe" in title_lower:
            score += 35
        if any(bad in url_lower for bad in ["scrimba.com", "github.com/mdn", "localhost", "/plus", "/curriculum/", "/blog/", "/learn/"]):
            score -= 100
        if profile == "canvas_animation" and self._rejection_reason(query, title_lower, url_lower, ""):
            score -= 100
        return score

    def _source_set_valid(self, sources, findings, query=""):
        profile = self._query_profile(query)
        relevant = [
            s for s in sources
            if s.get("status") == "fetched" and s.get("relevant") and not s.get("rejected")
        ]
        covered = set()
        for source in relevant:
            covered.update(source.get("topic_coverage", []))
        if len(relevant) < 2 or len(findings) < 2:
            return False
        if profile == "canvas_animation":
            return (
                "canvas" in covered
                and ("requestanimationframe" in covered or "animation/rendering" in covered)
            )
        if profile == "typescript_browser_architecture":
            required_topics = {
                "typescript",
                "javascript data structures",
                "queue/task scheduling",
                "browser/runtime",
                "testing/vitest",
                "state/modeling",
            }
            return len(covered & required_topics) >= 2
        query_coverage = {topic.split(":", 1)[1] for topic in covered if topic.startswith("query:")}
        return len(query_coverage) >= 2

    def perform_research(self, query, reason=None):
        results = {
            "status": "failed",
            "query": query,
            "reason": reason,
            "sources": [],
            "findings": [],
            "artifact_path": None,
            "errors": []
        }

        # 1. Choose backend - Playwright ONLY for research
        if not self.playwright.is_available():
            results["status"] = "blocked"
            results["errors"].append("Playwright research backend not available.")
            return results
        backend = self.playwright
        results["backend"] = "playwright"

        # 2. Run search variants and add known canonical docs candidates.
        search_url_template = self.research_config.get("search_url_template")
        links = []
        links.extend(self._canonical_candidates(query))
        search_errors = []
        for variant in self._query_variants(query):
            search_res = backend.run_search(variant, search_url_template)
            if "error" in search_res:
                search_errors.append(f"{variant}: {search_res['error']}")
                continue
            if search_res.get("links"):
                for l in search_res["links"]:
                    links.append({"url": l["url"], "title": l.get("title", "")})
            else:
                links.extend(self.parser.parse_links(search_res.get("html", "")))

        if not links:
            results["status"] = "failed"
            results["errors"].append("No search results found.")
            results["errors"].extend(search_errors)
            return results

        deduped = {}
        for link in links:
            url = link.get("url", "")
            if not url.startswith("http"):
                continue
            normalized = self._normalize_url(url)
            if normalized not in deduped:
                deduped[normalized] = {"url": normalized, "title": link.get("title", "")}

        scored_links = sorted(
            [(self._score_link(query, link), link) for link in deduped.values()],
            key=lambda item: item[0],
            reverse=True,
        )
        links = [link for score, link in scored_links if score > 0][:30]

        # 4. Fetch and extract top pages
        max_pages = self.research_config.get("max_pages_per_query", 8)
        for link in links[:max_pages]:
            print(f"Fetching result: {link['url']}")
            page_res = backend.fetch_page(link["url"])
            if "error" in page_res:
                results["sources"].append({
                    "title": link["title"],
                    "url": link["url"],
                    "status": "failed",
                    "notes": page_res["error"]
                })
                continue
                
            extracted = self.extractor.extract(link["url"], page_res["html"])
            excerpt_lower = extracted.get("excerpt", "").lower()
            title_lower = extracted.get("title", "").lower()
            coverage = self._topic_coverage(query, extracted.get("title", ""), extracted.get("url", ""), extracted.get("excerpt", ""))
            profile = self._query_profile(query)
            rejection_reason = ""
            if profile == "canvas_animation":
                rejection_reason = self._rejection_reason(query, title_lower, extracted.get("url", "").lower(), excerpt_lower)

            if rejection_reason:
                extracted["status"] = "failed"
                extracted["notes"] = rejection_reason

            is_relevant = bool(coverage)
            is_rejected = bool(rejection_reason)
            source_entry = {
                "title": extracted.get("title", link.get("title", "")),
                "url": extracted.get("url", link["url"]),
                "status": extracted.get("status", "failed"),
                "retrieved_at": extracted.get("retrieved_at", ""),
                "text_excerpt_path": extracted.get("cache_path", ""),
                "notes": extracted.get("notes", ""),
                "topic_coverage": coverage,
                "relevant": is_relevant and not is_rejected and extracted.get("status") == "fetched",
                "rejected": is_rejected,
            }

            if source_entry["relevant"]:
                results["findings"].append(extracted["excerpt"])
            else:
                if source_entry["status"] == "fetched":
                    source_entry["notes"] = (source_entry["notes"] + " low topic relevance").strip()

            results["sources"].append(source_entry)

        # 5. Final Validation
        results["query_profile"] = self._query_profile(query)
        results["source_set_relevance_passed"] = self._source_set_valid(results["sources"], results["findings"], query)
        if results["source_set_relevance_passed"]:
            results["status"] = "complete"
        elif results["findings"]:
            results["status"] = "partial"
            results["errors"].append("Research found relevant sources but did not satisfy source-set coverage requirements.")
        else:
            results["status"] = "failed"
            results["errors"].append("Research failed to find at least 2 relevant fetched sources with sufficient source-set coverage.")
            
        return results

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Studio Loop Browser Research CLI")
    parser.add_argument("--check", action="store_true", help="Check if research backend is available")
    parser.add_argument("--query", type=str, help="Perform research for the given query")
    parser.add_argument("--reason", type=str, help="Reason for research")
    
    args = parser.parse_args()
    
    # Load config if possible
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            
    researcher = BrowserResearch(config)
    
    if args.check:
        if researcher.playwright.is_available():
            print("Playwright available.")
            sys.exit(0)
        else:
            print("No research backend available (Playwright required).")
            sys.exit(1)
            
    if args.query:
        res = researcher.perform_research(args.query, args.reason)
        print(json.dumps(res, indent=2))
        if res["status"] != "complete":
            sys.exit(1)
        sys.exit(0)
    
    parser.print_help()
