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

if __name__ == "__main__":
    unittest.main()
