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
    Validates and normalises a URL to prevent duplicate crawling.

    Ensures the URL belongs to the target domain (internal link) and strips 
    any fragments (e.g., #section) or query parameters (e.g., ?sort=asc) 
    from the URL string.

    Args:
        url (str): The absolute URL to be normalised.
        base_netloc (str): The network location (domain) of the base website.

    Returns:
        Optional[str]: The cleaned URL if internal, or None if it is external.
    """
    parsed = urlparse(url)
    if parsed.netloc == base_netloc:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return None

def get_all_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    """
    Extracts, normalises, and deduplicates all internal links from an HTML page.

    Args:
        soup (BeautifulSoup): The parsed HTML content of the page.
        base_url (str): The URL of the current page being parsed.

    Returns:
        List[str]: A list of valid, unique internal URLs found on the page.
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
    """
    Fetches the HTML content of a given URL and parses it.

    Args:
        url (str): The URL to fetch.

    Returns:
        Optional[BeautifulSoup]: A parsed BeautifulSoup object if the request 
        is successful, or None if a network or HTTP error occurs.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {url}: {e}")
        return None

def enforce_politeness(visited_count: int) -> None:
    """
    Enforces a politeness delay between consecutive HTTP requests.

    Args:
        visited_count (int): The number of pages crawled so far. A delay is 
        only applied if this is greater than 0 (i.e., not the seed URL).
    """
    if visited_count > 0:
        print("Waiting 6 seconds to be polite...")
        time.sleep(6)

def crawl_website(seed_url: str) -> IndexType:
    """
    Coordinates the web crawling process using Breadth-First Search (BFS).

    Visits pages starting from the seed_url, respects politeness policies,
    extracts links to discover new pages, and builds an inverted index of 
    the text content found across the crawled pages.

    Args:
        seed_url (str): The initial URL to start crawling from.

    Returns:
        IndexType: A deeply nested dictionary representing the inverted index,
        mapping words to URLs and their corresponding frequency/positions.
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