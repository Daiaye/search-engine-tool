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


def find_query(index, query_words):
    """"
    Finds and returns a list of all pages that contain all the words in the query.
    """
    if not index:
        print("Error: The index is empty. Please 'build' or 'load' first.")
        return

    # Use intersection of sets to find pages containing all words
    matching_urls = None

    for word in query_words:
        if word not in index:
            # Maybe identify the word that cannot be found
            print(f"No pages found containing all the words: {', '.join(query_words)}")
            return
        
        urls_for_word = set(index[word].keys()) # keys are the urls

        if matching_urls is None:
            matching_urls = urls_for_word
        else:
            matching_urls = matching_urls & urls_for_word

    if matching_urls:
        ranked_results = []

        for url in matching_urls:
            total_score = 0
            for word in query_words:
                total_score += index[word][url]["frequency"]

            ranked_results.append((url, total_score))
        
        ranked_results.sort(key=lambda x: x[1], reverse=True)

        print(f"\nFound {len(matching_urls)} page(s) containing: {', '.join(query_words)}")
        for url, score in ranked_results:
            print(f" - {url} (Total Mentions: {score})")
    else:
        print(f"No pages found containing all the words: {', '.join(query_words)}")

    