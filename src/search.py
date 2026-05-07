from typing import Dict, List, Optional, Set, Tuple, Any

# Custom type alias for the inverted index
IndexType = Dict[str, Dict[str, Dict[str, Any]]]

def get_word_statistics(index: Optional[IndexType], word: str) -> Optional[List[Tuple[str, Dict[str, Any]]]]:
    """
    Returns the inverted index statistics for a specific word.
    Returns None if index is empty, or an empty list if word not found.
    """
    if not index:
        return None

    word = word.lower()
    if word in index:
        return list(index[word].items())
        
    return []

def get_missing_words(index: IndexType, query_words: List[str]) -> List[str]:
    """
    Helper function to identify any words from the search query 
    that are completely missing from the inverted index.
    """
    return [word for word in query_words if word not in index]

def get_matching_urls(index: IndexType, query_words: List[str]) -> Optional[Set[str]]:
    """
    Helper function that uses set intersection to find pages that contain ALL words in the query.
    """
    matching_urls: Optional[Set[str]] = None

    for word in query_words:        
        urls_for_word = set(index[word].keys()) # keys are the urls

        if matching_urls is None:
            matching_urls = urls_for_word
        else:
            matching_urls = matching_urls & urls_for_word
        
        # If no common pages, exit early
        if not matching_urls:
            break

    return matching_urls

def rank_results(index: IndexType, matching_urls: Set[str], query_words: List[str]) -> List[Tuple[str, int]]:
    """
    Helper function to calculate the total frequency score for each matching URL
    and return a list of (url, score) tuples sorted highest to lowest.
    """
    ranked_results: List[Tuple[str, int]] = []

    for url in matching_urls:
        total_score = 0
        for word in query_words:
            total_score += index[word][url]["frequency"]

        ranked_results.append((url, total_score))

    ranked_results.sort(key=lambda x: x[1], reverse=True)
    
    return ranked_results

def find_query(index: Optional[IndexType], query_words: List[str]) -> Tuple[Optional[List[str]], Optional[List[Tuple[str, int]]]]:
    """"
    Main function to find ranked search results for a multi-word query.
    Returns a tuple: (missing_words_list, ranked_results_list)
    """
    if not index:
        return None, None

    # Identify words that are not found in the crawled pages
    missing_words = get_missing_words(index, query_words)

    if missing_words:
        return missing_words, []

    # Find urls that contain all query words
    matching_urls = get_matching_urls(index, query_words)

    # Rank the results if any
    if matching_urls:
        ranked_results = rank_results(index, matching_urls, query_words)
        return [], ranked_results

    return [], []