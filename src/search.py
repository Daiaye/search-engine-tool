import json

def print_word(index, word):
    """
    Prints the inverted index for a particular word.
    """
    if not index:
        print("Error: The index is empty. Please 'build' or 'load' first.")
        return

    if word in index:
        print(f"\n--- Statistics for '{word}' ---")
        word_data = index[word]

        for url, stats in word_data.items():
            frequency = stats["frequency"]
            positions = stats["positions"]
            print(f"URL: {url}")
            print(f"  - Frequency: {frequency}")
            print(f"  - Positions: {positions}")
        print("-------------------------------")
    else:
        print(f"The word '{word}' was not found in any crawled pages.")

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
    Main function to find and print ranked search results for a multi-word query.
    """
    if not index:
        print("Error: The index is empty. Please 'build' or 'load' first.")
        return

    # Identify words that are not found in the crawled pages
    missing_words = get_missing_words(index, query_words)

    if missing_words:
        print(f"Search failed. The following word(s) were never found during crawling: {', '.join(missing_words)}")
        return

    # Find urls that contain all query words
    matching_urls = get_matching_urls(index, query_words)

    # Rank the results if any
    if matching_urls:
        ranked_results = rank_results(index, matching_urls, query_words)

        print(f"\nFound {len(matching_urls)} page(s) containing: {', '.join(query_words)}")

        for url, score in ranked_results:
            print(f" - {url} (Total Mentions: {score})")
    else:
        print(f"No pages found containing all the words: {', '.join(query_words)}")

    