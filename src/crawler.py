import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.indexer import index_page_content
from collections import deque

def get_all_links(soup, base_url):
    """
    Extracts all valid links, converts to absolute URLs,
    removes fragments/queries, and filters for internal links only.
    """
    links = []
    links_set = set()
    base_netloc = urlparse(base_url).netloc # netloc is 'Network Location' or domain

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url)

        if parsed.netloc == base_netloc:
            # Strip fragments and query parameters to prevent duplicate indexing
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            if clean_url not in links_set:
                links.append(clean_url)
                links_set.add(clean_url)
        
    return links

def crawl_website(seed_url):
    """
    Crawls the target website, respecting the 6-second politeness window.
    Returns the compiled inverted index.
    """
    frontier = deque([seed_url])
    frontier_set = {seed_url} # To check if a link is already in frontier in O(1)
    visited = set()       
    
    inverted_index = {}   

    print(f"Starting crawl at {seed_url}...")

    # TODO: Remove testing limit 'len(visited) < 3'
    while frontier and len(visited) < 3:
        current_url = frontier.popleft()

        if current_url in visited:
            continue

        print(f"\nCrawling: {current_url}")
        
        # Enforce politeness
        if len(visited) > 0:
            print("Waiting 6 seconds to be polite...")
            time.sleep(6)

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status() # Raise an exception if the server returns an error (e.g., 404 Not Found)

            visited.add(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            new_links = get_all_links(soup, current_url)
            for link in new_links:
                if link not in visited and link not in frontier_set:
                    frontier.append(link)
                    frontier_set.add(link)
                    
            print(f"Found {len(new_links)} valid links on this page. Frontier size: {len(frontier)}")

            inverted_index = index_page_content(soup, current_url, inverted_index)

        except requests.exceptions.RequestException as e:
            print(f"Failed to crawl {current_url}: {e}")

    print("\nCrawling complete!")
    print(f"Total pages visited: {len(visited)}")
    return inverted_index


# TEMPORARY TEST BLOCK
if __name__ == "__main__":
    print("Running a quick 3-page test...")
    crawl_website("https://quotes.toscrape.com/")