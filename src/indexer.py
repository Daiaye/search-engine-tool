import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# Custom type alias for the inverted index
IndexType = Dict[str, Dict[str, Dict[str, Any]]]

def clean_text(soup: BeautifulSoup) -> List[str]:
    """
    Extracts and cleans visible text from an HTML document.

    Removes structural noise like scripts, styles, and meta tags. 
    Converts all remaining text to lowercase, strips punctuation using 
    regular expressions, and splits the content into individual words.

    Args:
        soup (BeautifulSoup): The parsed HTML document to clean.

    Returns:
        List[str]: A chronological list of cleaned words extracted from the page.
    """
    for element in soup(["script", "style", "meta", "noscript"]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True).lower()
    
    # Remove punctuation with regex
    cleaned_string = re.sub(r'[^\w\s]', ' ', text).strip()
    words_list = cleaned_string.split()

    return words_list

def index_page_content(soup: BeautifulSoup, current_url: str, inverted_index: IndexType) -> IndexType:
    """
    Processes a page's HTML to extract words and update the global inverted index.

    Calculates word occurrences and their exact positional indices on the current 
    page, then updates the shared inverted index structure accordingly.

    Args:
        soup (BeautifulSoup): The parsed HTML of the current page.
        current_url (str): The URL of the page being indexed.
        inverted_index (IndexType): The current state of the global inverted index.

    Returns:
        IndexType: The updated inverted index incorporating data from this page.
    """
    words = clean_text(soup)

    for position, word in enumerate(words):
        # We haven't seen the word before at all
        if word not in inverted_index:
            inverted_index[word] = {}

        # We have seen the word, but not on this page
        if current_url not in inverted_index[word]:
            inverted_index[word][current_url] = {
                "frequency": 0,
                "positions": []
            }
        
        # Add statistics
        inverted_index[word][current_url]["frequency"] += 1
        inverted_index[word][current_url]["positions"].append(position)

    return inverted_index