import sys
import os
import tempfile
sys.path.append(os.path.join(os.getcwd(), ".agent/orchestrator"))
from page_extractor import PageExtractor

def test_page_extractor_does_not_flag_clean_mdn_text():
    text = "<html><title>Window: requestAnimationFrame()</title><body>Canvas animation uses requestAnimationFrame for smooth rendering.</body></html>"
    with tempfile.TemporaryDirectory() as temp_dir:
        result = PageExtractor({}, temp_dir).extract("https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame", text)
        print(f"Status: {result['status']}")
        assert result["status"] == "fetched"
    print("Regression test PASSED")

if __name__ == "__main__":
    test_page_extractor_does_not_flag_clean_mdn_text()
