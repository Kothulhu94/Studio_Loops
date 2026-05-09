import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.agent/orchestrator")))

from browser_research import BrowserResearch
from studio_loop import StudioLoopOrchestrator


FORBIDDEN = [
    "VRDisplay",
    "XRSession",
    "WebXR",
    "Deprecated",
    "Experimental",
    "Non-standard",
    "Limited availability",
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


def main():
    os.environ.pop("HARNESS_VERIFICATION_MODE", None)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    orchestrator = StudioLoopOrchestrator(base_path)
    researcher = BrowserResearch(orchestrator.config, base_path)

    if not researcher.playwright.is_available():
        print("SKIP: Playwright/Chromium is not available.")
        return 0

    result = researcher.perform_research("MDN Canvas API requestAnimationFrame")
    combined = "\n".join(
        [str(result)]
        + [source.get("title", "") + " " + source.get("url", "") + " " + source.get("notes", "") for source in result.get("sources", [])]
        + result.get("findings", [])
    )

    assert result.get("status") == "complete", result
    assert result.get("backend") == "playwright", result
    assert result.get("source_set_relevance_passed") is True, result
    assert len([s for s in result.get("sources", []) if s.get("status") == "fetched" and s.get("relevant")]) >= 2, result
    for forbidden in FORBIDDEN:
        assert forbidden not in combined, forbidden

    print("PASS: Real Playwright browser research completed cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
