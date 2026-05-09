import re

class SourceSummarizer:
    def __init__(self, config=None):
        self.config = config or {}

    def summarize(self, html_content):
        # Basic HTML stripping and fact extraction logic
        # In a real scenario, this might call the local model to summarize
        # or use a library like BeautifulSoup (which might not be available)
        
        # Simple regex-based strip
        text = re.sub('<[^<]+?>', '', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Return first 2000 characters as a "snippet"
        return text[:2000]
