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

def test_page_extractor_flags_visible_mojibake():
    corrupted = (
        "<html><title>Canvas API</title><body>"
        "It\u00e2\u20ac\u2122s been available. "
        "The context\u00e2\u20ac\u201dthe thing to draw on."
        "</body></html>"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        result = PageExtractor({}, temp_dir).extract("https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API", corrupted)
        print(f"Corrupt status: {result['status']}")
        assert result["status"] == "failed"
    print("Mojibake regression test PASSED")

if __name__ == "__main__":
    test_page_extractor_does_not_flag_clean_mdn_text()
    test_page_extractor_flags_visible_mojibake()
