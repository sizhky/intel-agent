"""Google Custom Search client for competitor research."""

from typing import List, Dict, Optional
import requests

from intel_agent.core.config import config

class GoogleSearchClient:
    """Client for Google Custom Search API."""
    
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self, api_key: str, cx: Optional[str] = None):
        """Initialize the search client.
        
        Args:
            api_key: Google Custom Search API key
            cx: Custom Search Engine ID (optional)
        """
        self.api_key = api_key
        self.cx = cx or config.search_engine_id
        
        if not self.cx:
            raise ValueError("Custom Search Engine ID (cx) is required")
    
    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """Perform a Google search.
        
        Args:
            query: Search query string
            num_results: Number of results to return (max 10 per request)
            
        Returns:
            List of search results, each containing title, link, and snippet
        """
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": min(num_results, 10),  # API limit is 10 per request
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        if "items" not in data:
            return []
            
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": "google",
            }
            for item in data["items"]
        ]
    
    def search_competitors(self, domain: str, num_results: int = 10) -> List[Dict]:
        """Search for competitors in a specific domain.
        
        Args:
            domain: Business domain/industry to search within
            num_results: Number of results to return
            
        Returns:
            List of potential competitors with their details
        """
        # Craft an effective search query for finding competitors
        query = f"top companies competitors {domain} industry review"
        
        try:
            results = self.search(query, num_results)
            return results
        except requests.RequestException as e:
            print(f"Error searching for competitors: {e}")
            return []
