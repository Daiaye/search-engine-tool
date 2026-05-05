import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from indexer import index_page_content

def get_all_links(soup, base_url):
    """
    Extracts all valid links, converts to absolute URLs,
    removes fragments/queries, and filters for internal links only.
    """
    links = []
    base_netloc = urlparse(base_url).netloc # netloc is 'Network Location' or domain

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Convert relative URLs to absolute URLs
        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url)
        if parsed.netloc == base_netloc:
            # Reconstruct URL without query and fragment
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            if clean_url not in links:
                links.append(clean_url)
        
    return links

def crawl_website(seed_url):
    """
    Crawls the target website, respecting the 6-second politeness window.
    Returns the compiled inverted index.
    """
    frontier = [seed_url] # "To-Do" list
    visited = set()       # Memory to avoid infinite loops
    
    inverted_index = {}   

    print(f"Starting crawl at {seed_url}...")

    # Remove len(visited) < 3 when done with testing
    while frontier and len(visited) < 3:
        # Get the next URL from the frontier
        current_url = frontier.pop(0)

        if current_url in visited:
            continue

        print(f"\nCrawling: {current_url}")
        
        # 1. THE POLITENESS WINDOW
        # We sleep BEFORE the request so we don't accidentally spam the server
        if len(visited) > 0:
            print("Waiting 6 seconds to be polite...")
            time.sleep(6)

        try:
            # 2. Fetch the HTML
            response = requests.get(current_url, timeout=10)
            # Raise an exception if the server returns an error (e.g., 404 Not Found)
            response.raise_for_status() 
            
            # Mark as visited only after a successful fetch
            visited.add(current_url)

            # 3. Parse the HTML using Beautiful Soup
            soup = BeautifulSoup(response.text, 'html.parser')

            # 4. Find new links and add them to the frontier
            new_links = get_all_links(soup, current_url)
            for link in new_links:
                if link not in visited and link not in frontier:
                    frontier.append(link)
                    
            print(f"Found {len(new_links)} valid links on this page. Frontier size: {len(frontier)}")

            # 5. Index the words on this page
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