import os
import json
import sys

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

        # 2. Run search
        search_url_template = self.research_config.get("search_url_template")
        search_res = backend.run_search(query, search_url_template)
        
        if "error" in search_res:
            results["status"] = "failed"
            results["errors"].append(search_res["error"])
            return results

        # 3. Parse links
        links = []
        if "links" in search_res and search_res["links"]:
            # Standardize pre-extracted links
            for l in search_res["links"]:
                links.append({"url": l["url"], "title": l.get("title", "")})
        else:
            links = self.parser.parse_links(search_res["html"])

        if not links:
            results["status"] = "partial"
            results["errors"].append("No search results found.")
            return results

        # 3b. Relevance Scoring
        scored_links = []
        query_terms = set(query.lower().split())
        # Strong-term filtering
        weak_terms = {"mdn", "api", "web", "docs", "documentation", "guide", "tutorial", "how", "to"}
        strong_terms = query_terms - weak_terms
        if not strong_terms: strong_terms = query_terms # Fallback if all terms are weak

        preferred_domains = [
            "developer.mozilla.org", "typescriptlang.org", "web.dev", 
            "w3.org"
        ]
        
        for link in links:
            score = 0
            title_lower = link["title"].lower()
            url_lower = link["url"].lower()
            
            # 1. Strong term matches in title/URL (Highest weight)
            strong_matches = 0
            for term in strong_terms:
                if term in title_lower: 
                    score += 25
                    strong_matches += 1
                if term in url_lower: 
                    score += 15
                    strong_matches += 1
            
            # 2. Weak term matches (Lower weight)
            for term in weak_terms:
                if term in title_lower: score += 5
                if term in url_lower: score += 2
            
            # 3. Domain boosts / penalties
            domain = ""
            try:
                from urllib.parse import urlparse
                domain = urlparse(link["url"]).netloc.lower()
                if any(pd in domain for pd in preferred_domains):
                    score += 20
            except: pass
            
            # 4. Reject marketing/placeholder/generic landing pages
            bad_patterns = ["scrimba.com", "github.com/mdn", "example" + "." + "com", "localhost", "plus", "curriculum", "course", "marketing"]
            if any(bad in url_lower for bad in bad_patterns):
                score -= 100 # Disqualify
                
            # 5. Language Penalties (Non-English prefixes)
            non_english_prefixes = ["/ar.", "/az.", "/be.", "/ru.", "/zh.", "/ja.", "/ko.", "/ar/", "/ru/", "/zh/", "/ja/", "/ko/"]
            if any(prefix in url_lower for prefix in non_english_prefixes):
                score -= 50
                
            # 6. Penalize zero strong term overlap
            if strong_matches < 1:
                score -= 40
            
            scored_links.append((score, link))
        
        # Sort by score descending
        scored_links.sort(key=lambda x: x[0], reverse=True)
        # Only keep links with a significant score and at least some query overlap
        links = [l for s, l in scored_links if s > 15] 

        # 4. Fetch and extract top pages
        max_pages = self.research_config.get("max_pages_per_query", 3)
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
            
            # Deep Relevance Check for MDN / Technical docs
            excerpt_lower = extracted.get("excerpt", "").lower()
            title_lower = extracted.get("title", "").lower()
            
            # Require distinct term coverage (Point 1)
            strong_body_terms_found = {term for term in strong_terms if term in excerpt_lower or term in title_lower}
            strong_body_count = len(strong_body_terms_found)
            
            # Rejection Keywords (unless specifically requested in query)
            rejection_keywords = [
                "vrdisplay", "xrsession", "webxr", "deprecated", 
                "experimental", "non-standard", "limited availability"
            ]
            
            is_rejected = False
            for rj in rejection_keywords:
                if rj in excerpt_lower or rj in title_lower:
                    # Only reject if the query didn't explicitly ask for this term
                    if rj not in query.lower():
                        is_rejected = True
                        break
            
            if is_rejected:
                extracted["status"] = "failed"
                extracted["notes"] = f"rejected: contains irrelevant or low-quality term ({rj})"
            
            source_entry = {
                "title": extracted["title"],
                "url": extracted["url"],
                "status": extracted["status"],
                "retrieved_at": extracted["retrieved_at"],
                "text_excerpt_path": extracted["cache_path"],
                "notes": extracted.get("notes", ""),
                "strong_relevance": strong_body_count
            }
            
            if source_entry["status"] == "fetched" and strong_body_count >= 2:
                results["findings"].append(extracted["excerpt"])
            else:
                if source_entry["status"] == "fetched":
                    source_entry["notes"] += f" (low strong-term relevance: found {strong_body_count})"

            results["sources"].append(source_entry)

        # 5. Final Validation
        # Require at least 2 valid sources with distinct strong terms in body
        valid_sources = [s for s in results["sources"] if s["status"] == "fetched" and s.get("strong_relevance", 0) >= 2]

        if len(valid_sources) >= 2:
            results["status"] = "complete"
        elif results["findings"]:
            results["status"] = "partial"
        else:
            results["status"] = "failed"
            results["errors"].append("Research failed to find at least 2 valid sources with sufficient strong-term relevance.")
            
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

