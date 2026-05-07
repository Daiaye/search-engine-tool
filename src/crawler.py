import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.indexer import index_page_content
from collections import deque
from typing import Optional, List, Dict, Any, Set

# Custom type alias for the inverted index
IndexType = Dict[str, Dict[str, Dict[str, Any]]]

def normalise_url(url: str, base_netloc: str) -> Optional[str]:
    """
    Validates if a URL is internal and returns a version without fragments or queries to prevent duplicate crawling of the same page.
    Returns None if the URL is external.
    """
    parsed = urlparse(url)
    if parsed.netloc == base_netloc:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return None

def get_all_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    """
    Extracts and normalises all internal links.
    """
    links: List[str] = []
    links_set: Set[str] = set()
    base_netloc = urlparse(base_url).netloc # netloc is 'Network Location' or domain

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        absolute_url = urljoin(base_url, href)
        clean_url = normalise_url(absolute_url, base_netloc)
           
        if clean_url and clean_url not in links_set:
            links.append(clean_url)
            links_set.add(clean_url)
        
    return links

def fetch_page(url: str) -> Optional[BeautifulSoup]:
    """Handles the network request and returns a BeautifulSoup object or None on failure."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {url}: {e}")
        return None

def enforce_politeness(visited_count: int) -> None:
    """Wait for the required 6-second window if this is not the first request."""
    if visited_count > 0:
        print("Waiting 6 seconds to be polite...")
        time.sleep(6)

def crawl_website(seed_url: str) -> IndexType:
    """
    Coordinates the crawling process using BFS.
    """
    frontier = deque([seed_url])
    frontier_set: Set[str] = {seed_url} # To check if a link is already in frontier in O(1)
    visited: Set[str] = set()       
    inverted_index: IndexType = {}   

    print(f"Starting crawl at {seed_url}...")

    # TODO: Remove testing limit 'len(visited) < 3'
    while frontier and len(visited) < 3:
        current_url = frontier.popleft()

        if current_url in visited:
            continue

        enforce_politeness(len(visited))

        print(f"\nCrawling: {current_url}")

        soup = fetch_page(current_url)

        if soup:
            visited.add(current_url)

            # Extract and queue new links
            new_links = get_all_links(soup, current_url)
            for link in new_links:
                if link not in visited and link not in frontier_set:
                    frontier.append(link)
                    frontier_set.add(link)
            
            print(f"Found {len(new_links)} valid links on this page. Frontier size: {len(frontier)}")

            inverted_index = index_page_content(soup, current_url, inverted_index)

    print(f"\nCrawling complete! Total pages visited: {len(visited)}")
    return inverted_index

# TEMPORARY TEST BLOCK
if __name__ == "__main__":
    print("Running a quick 3-page test...")
    crawl_website("https://quotes.toscrape.com/")