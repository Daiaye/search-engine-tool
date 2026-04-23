import re
from bs4 import BeautifulSoup

def clean_text(soup: BeautifulSoup):
    """
    Extracts text from the HTML, makes it case-insensitive, 
    removes punctuation, and splits it into a list of words.
    """
    text = soup.get_text(separator=" ", strip=True).lower()
    
    # Remove punctuation with regex
    cleaned_string = re.sub(r'[^\w\s]', ' ', text).strip()
    words_list = cleaned_string.split()

    return words_list

def index_page_content(soup, current_url, inverted_index):
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
