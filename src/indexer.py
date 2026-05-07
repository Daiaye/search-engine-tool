import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

# Custom type alias for the inverted index
IndexType = Dict[str, Dict[str, Dict[str, Any]]]

def clean_text(soup: BeautifulSoup) -> List[str]:
    """
    Extracts clean text from HTML by removing noise (scripts, styles),
    converting to lowercase, stripping punctuation, and splitting into words.
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
    Takes the parsed HTML, extracts the words, and updates the inverted index
    with the frequency and positions of each word on this specific page.
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