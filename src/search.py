def get_word_statistics(index, word):
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

def get_missing_words(index, query_words):
    """
    Helper function to identify any words from the search query 
    that are completely missing from the inverted index.
    """
    return [word for word in query_words if word not in index]

def get_matching_urls(index, query_words):
    """
    Helper function that uses set intersection to find pages that contain ALL words in the query.
    """
    matching_urls = None

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

def rank_results(index, matching_urls, query_words):
    """
    Helper function to calculate the total frequency score for each matching URL
    and return a list of (url, score) tuples sorted highest to lowest.
    """
    ranked_results = []

    for url in matching_urls:
        total_score = 0
        for word in query_words:
            total_score += index[word][url]["frequency"]

        ranked_results.append((url, total_score))

    ranked_results.sort(key=lambda x: x[1], reverse=True)
    
    return ranked_results

def find_query(index, query_words):
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
    