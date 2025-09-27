from crewai.tools import BaseTool
from pydantic import Field
from typing import Optional
import os
import requests
import time

class BraveSearchTool(BaseTool):
    name: str = "brave_search"
    description: str = "Search the web using Brave Search API. Input should be a search query string."
    api_key: Optional[str] = Field(default_factory=lambda: os.environ.get("BRAVE_API_KEY"))
    last_request_time: Optional[float] = None

    def _run(self, query: str) -> str:
        """Execute the search using Brave Search API."""
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not found in environment variables. Please set it in your .env file.")

        if self.last_request_time:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': self.api_key,
        }
        params = {'q': query}
        
        try:
            response = requests.get(
                'https://api.search.brave.com/res/v1/web/search',
                headers=headers,
                params=params,
                timeout=10
            )
            self.last_request_time = time.time()
            response.raise_for_status()
            results = response.json()
            
            # Format the results as a string
            formatted_results = []
            # Get top 10 results, or fewer if not available
            for web in results.get('web', {}).get('results', [])[:10]:
                formatted_results.append(f"Title: {web['title']}\nURL: {web['url']}\nDescription: {web['description']}\n")
            
            if not formatted_results:
                return "No results found for the query."

            return "\n\n".join(formatted_results)
            
        except requests.exceptions.RequestException as e:
            return f"Error performing search: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Async version of _run is not implemented for this tool."""
        # The `_arun` method is not used in this crew, so we can leave it as not implemented.
        raise NotImplementedError("BraveSearchTool does not support async execution.")