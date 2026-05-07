from typing import Dict, List, Optional, Set, Tuple, Any

# Custom type alias for the inverted index
IndexType = Dict[str, Dict[str, Dict[str, Any]]]

def get_word_statistics(index: Optional[IndexType], word: str) -> Optional[List[Tuple[str, Dict[str, Any]]]]:
    """
    Retrieves indexing statistics (frequency and positions) for a specific word.

    Args:
        index (Optional[IndexType]): The loaded inverted index dictionary.
        word (str): The word to query in the index.

    Returns:
        Optional[List[Tuple[str, Dict[str, Any]]]]: A list of tuples containing the 
        URL and its associated statistics. Returns None if the index is empty, 
        or an empty list if the word is not found.
    """
    if not index:
        return None

    word = word.lower()
    if word in index:
        return list(index[word].items())
        
    return []

def get_missing_words(index: IndexType, query_words: List[str]) -> List[str]:
    """
    Identifies words from a search query that are absent from the entire index.

    Args:
        index (IndexType): The loaded inverted index dictionary.
        query_words (List[str]): A list of lowercase words from the search query.

    Returns:
        List[str]: A list of query words that do not exist in the index.
    """
    return [word for word in query_words if word not in index]

def get_matching_urls(index: IndexType, query_words: List[str]) -> Optional[Set[str]]:
    """
    Finds URLs that contain ALL the words specified in a search query.

    Utilises set intersection to efficiently filter down the URLs that share
    all words in the multi-word query. Exits early if an intersection is empty.

    Args:
        index (IndexType): The loaded inverted index dictionary.
        query_words (List[str]): A list of lowercase words from the search query.

    Returns:
        Optional[Set[str]]: A set of URLs containing all query words, or None if 
        no such URLs exist.
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
    Ranks a set of matching URLs based on the total frequency of query words.

    Args:
        index (IndexType): The loaded inverted index dictionary.
        matching_urls (Set[str]): A set of URLs known to contain all query words.
        query_words (List[str]): A list of lowercase words from the search query.

    Returns:
        List[Tuple[str, int]]: A list of (URL, total_score) tuples, sorted in 
        descending order of their total score.
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
    """
    Orchestrates a multi-word search query against the inverted index.

    Identifies any missing words to prevent unnecessary computation. If all words 
    exist in the index, it finds pages containing all words and ranks them by 
    their total frequency scores.

    Args:
        index (Optional[IndexType]): The loaded inverted index dictionary.
        query_words (List[str]): A list of lowercase words from the user's query.

    Returns:
        Tuple[Optional[List[str]], Optional[List[Tuple[str, int]]]]: A tuple where 
        the first element is a list of missing words (if any), and the second is 
        a ranked list of (URL, score) tuples.
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