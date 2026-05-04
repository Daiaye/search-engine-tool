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