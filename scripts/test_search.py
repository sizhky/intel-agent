"""Test script for Google Custom Search functionality."""

from intel_agent.core.config import config
from intel_agent.core.search import GoogleSearchClient

def test_search():
    """Test the search functionality."""
    # Initialize the search client
    client = GoogleSearchClient(api_key=config.search_api_key, cx=config.search_engine_id)
    
    # Test domain
    test_domain = "AI chatbot companies"
    
    print(f"\nSearching for competitors in: {test_domain}")
    print("-" * 50)
    
    # Search for competitors
    results = client.search_competitors(test_domain, num_results=5)
    
    # Display results
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['link']}")
        print(f"   Summary: {result['snippet']}")

if __name__ == "__main__":
    # Skip full validation for now, just check search-related configs
    if not config.search_api_key or not config.search_engine_id:
        print("Please configure SEARCH_API_KEY and SEARCH_ENGINE_ID in your .env file.")
    else:
        test_search()
