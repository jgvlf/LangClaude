"""
Web search and fetch tools using LangChain built-ins and custom implementations.

Provides web search using DuckDuckGo and content fetching capabilities.
"""

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests
from bs4 import BeautifulSoup


# LangChain's built-in DuckDuckGo search tool
web_search = DuckDuckGoSearchRun()


# Configure requests headers to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


@tool
def web_fetch(url: str, timeout: int = 10) -> str:
    """
    Fetch and extract text content from a URL.
    
    Args:
        url: The URL to fetch content from.
        timeout: Request timeout in seconds (default: 10).
    
    Returns:
        The extracted text content from the URL.
    """
    try:
        # Ensure URL has a protocol
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up excessive whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n'.join(lines)
        
        # Limit content to avoid too large responses
        max_chars = 5000
        if len(content) > max_chars:
            content = content[:max_chars] + f"\n\n[Content truncated - showing first {max_chars} characters]"
        
        return f"Content from {url}:\n\n{content}"
    
    except requests.exceptions.MissingSchema:
        return f"Error: Invalid URL format: {url}"
    except requests.exceptions.ConnectionError:
        return f"Error: Unable to connect to {url}"
    except requests.exceptions.Timeout:
        return f"Error: Request timeout while fetching {url}"
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP {e.response.status_code} when fetching {url}"
    except Exception as e:
        return f"Error fetching content from {url}: {str(e)}"
