import unittest
import json
import os
import sys
from unittest.mock import MagicMock, patch

# Add orchestrator to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator"))
from browser_research import BrowserResearch

class TestBrowserResearchMock(unittest.TestCase):
    def setUp(self):
        self.fixture_path = os.path.join(os.path.dirname(__file__), "fixtures/research_mdn_requestanimationframe.json")
        with open(self.fixture_path, 'r') as f:
            self.mock_data = json.load(f)

    @patch('browser_research.PlaywrightResearch')
    def test_perform_research_with_mock_backend(self, mock_playwright_class):
        # Setup mock backend
        mock_backend = MagicMock()
        mock_playwright_class.return_value = mock_backend
        mock_backend.is_available.return_value = True
        
        # Simulate search results
        mock_backend.run_search.return_value = {"html": "<html>MDN Canvas requestAnimationFrame</html>"}
        
        # We also need to mock SearchResultParser to return the URLs in the fixture
        with patch('browser_research.SearchResultParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            mock_parser.parse_links.return_value = [
                {"title": s["title"], "url": s["url"]} for s in self.mock_data["sources"]
            ]
            
            # Mock PageExtractor or just the fetch_page/extractor logic
            mock_backend.fetch_page.return_value = {"html": "Dummy MDN content"}
            
            with patch('browser_research.PageExtractor') as mock_extractor_class:
                mock_extractor = MagicMock()
                mock_extractor_class.return_value = mock_extractor
                
                # Setup side effects for extraction to return fixture-like data
                def extract_side_effect(url, html):
                    for s in self.mock_data["sources"]:
                        if s["url"] == url:
                            return {
                                "title": s["title"],
                                "url": s["url"],
                                "status": "fetched",
                                "retrieved_at": "2026-05-09",
                                "cache_path": f".agent/cache/{url.split('/')[-1]}.txt",
                                "excerpt": "Found MDN Canvas requestAnimationFrame content here.",
                                "notes": ""
                            }
                    return {"status": "failed", "error": "Not found"}
                
                mock_extractor.extract.side_effect = extract_side_effect
                
                researcher = BrowserResearch()
                results = researcher.perform_research("MDN Canvas API requestAnimationFrame")
                
                self.assertEqual(results["status"], "complete")
                self.assertTrue(len(results["sources"]) >= 2)
                self.assertTrue(len(results["findings"]) >= 1)

    def test_canvas_source_set_still_requires_canvas_and_animation_coverage(self):
        researcher = BrowserResearch()
        sources_missing_animation = [
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["canvas"]},
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["canvas", "2d context"]},
        ]
        sources_complete = [
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["canvas"]},
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["requestanimationframe"]},
        ]

        self.assertFalse(
            researcher._source_set_valid(
                sources_missing_animation,
                ["finding one", "finding two"],
                "MDN Canvas API requestAnimationFrame",
            )
        )
        self.assertTrue(
            researcher._source_set_valid(
                sources_complete,
                ["finding one", "finding two"],
                "MDN Canvas API requestAnimationFrame",
            )
        )

    def test_typescript_browser_task_queue_passes_without_canvas_coverage(self):
        researcher = BrowserResearch()
        sources = [
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["typescript", "state/modeling"]},
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["javascript data structures", "queue/task scheduling", "testing/vitest"]},
        ]

        self.assertTrue(
            researcher._source_set_valid(
                sources,
                ["TypeScript interfaces model state.", "Array queues can be tested with Vitest."],
                "TypeScript browser task queue data model Vitest unit test",
            )
        )

    def test_generic_technical_query_uses_query_term_overlap_not_canvas(self):
        researcher = BrowserResearch()
        sources = [
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["query:pathfinding", "query:grid"]},
            {"status": "fetched", "relevant": True, "rejected": False, "topic_coverage": ["query:grid", "query:algorithm"]},
        ]

        self.assertTrue(
            researcher._source_set_valid(
                sources,
                ["Pathfinding grid note.", "Algorithm grid note."],
                "pathfinding grid algorithm",
            )
        )

    def test_query_aware_canonical_candidates_include_typescript_vitest_mdn_js(self):
        researcher = BrowserResearch()
        candidates = researcher._canonical_candidates("TypeScript browser task queue data model Vitest unit test")
        urls = [candidate["url"] for candidate in candidates]

        self.assertTrue(any("typescriptlang.org/docs/handbook" in url for url in urls))
        self.assertTrue(any("Global_Objects/Array" in url for url in urls))
        self.assertTrue(any("Global_Objects/Map" in url for url in urls))
        self.assertTrue(any("vitest.dev/guide" in url for url in urls))

    @patch('browser_research.PlaywrightResearch')
    def test_typescript_browser_research_can_complete_with_relevant_sources(self, mock_playwright_class):
        mock_backend = MagicMock()
        mock_playwright_class.return_value = mock_backend
        mock_backend.is_available.return_value = True
        mock_backend.run_search.return_value = {"links": []}
        mock_backend.fetch_page.return_value = {"html": "ok"}

        with patch('browser_research.PageExtractor') as mock_extractor_class:
            mock_extractor = MagicMock()
            mock_extractor_class.return_value = mock_extractor

            def extract_side_effect(url, html):
                if "typescriptlang" in url:
                    return {
                        "title": "TypeScript Handbook Object Types",
                        "url": url,
                        "status": "fetched",
                        "retrieved_at": "2026-05-09",
                        "cache_path": ".agent/cache/typescript.txt",
                        "excerpt": "TypeScript interface type alias generics object data model state.",
                        "notes": "",
                    }
                if "Array" in url or "Map" in url:
                    return {
                        "title": "JavaScript Array Map queue data structures",
                        "url": url,
                        "status": "fetched",
                        "retrieved_at": "2026-05-09",
                        "cache_path": ".agent/cache/js.txt",
                        "excerpt": "Array Map object queue fifo priority task scheduler browser unit test.",
                        "notes": "",
                    }
                if "vitest" in url:
                    return {
                        "title": "Vitest unit test API",
                        "url": url,
                        "status": "fetched",
                        "retrieved_at": "2026-05-09",
                        "cache_path": ".agent/cache/vitest.txt",
                        "excerpt": "Vitest describe test expect unit test browser code.",
                        "notes": "",
                    }
                return {"status": "failed", "error": "not used"}

            mock_extractor.extract.side_effect = extract_side_effect
            researcher = BrowserResearch()
            results = researcher.perform_research("TypeScript browser task queue data model Vitest unit test")

            self.assertEqual(results["query_profile"], "typescript_browser_architecture")
            self.assertEqual(results["status"], "complete")
            self.assertTrue(results["source_set_relevance_passed"])
            self.assertGreaterEqual(
                len([s for s in results["sources"] if s.get("status") == "fetched" and s.get("relevant")]),
                2,
            )

if __name__ == "__main__":
    unittest.main()
