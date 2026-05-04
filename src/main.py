import sys
import json
import os
from crawler import crawl_website
from search import get_word_statistics, find_query

INDEX_FILE_PATH = os.path.join("data", "index.json")

def main():
    print("Welcome to the COMP3011 Search Engine Tool")
    print("Available commands: build, load, print <word>, find <query...>, exit")
    
    current_index = None # Holds the index in memory once loaded

    while True:
        try:
            user_input = input("> ").strip().split()
            
            if not user_input:
                continue
            
            command = user_input[0].lower()
            args = user_input[1:]

            if command == "build":
                print("Crawling https://quotes.toscrape.com/ and building the index...")
                current_index = crawl_website("https://quotes.toscrape.com/")

                # Ensure the data folder exists before saving
                os.makedirs(os.path.dirname(INDEX_FILE_PATH), exist_ok=True)

                # Save index to disk
                with open(INDEX_FILE_PATH, "w", encoding="utf-8") as f:
                    json.dump(current_index, f, indent=4)

                print(f"Index built and saved to {INDEX_FILE_PATH}")

            elif command == "load":
                print("Loading index from file system...")
                
                if os.path.exists(INDEX_FILE_PATH):
                    with open(INDEX_FILE_PATH, "r", encoding="utf-8") as f:
                        current_index = json.load(f)
                    print(f"Index loaded successfully! Your search engine knows {len(current_index)} unique words.")
                else:
                    print("Error: No saved index found. Please run 'build' first.")

            elif command == "print":
                if not args:
                    print("Error: Please provide a word. Example: print nonsense")
                    continue
                
                word = args[0].lower() # Case-insensitive search
                print(f"Fetching index data for: '{word}'")
                stats = get_word_statistics(current_index, word)

                if stats is None:
                    print("Error: The index is empty. Please 'build' or 'load' first.")
                elif not stats:
                    print(f"The word '{word}' was not found in any crawled pages.")
                else:
                    print(f"\n--- Statistics for '{word}' ---")
                    for url, stat_data in stats:
                        print(f"URL: {url}")
                        print(f"  - Frequency: {stat_data['frequency']}")
                        print(f"  - Positions: {stat_data['positions']}")
                    print("-------------------------------")
                
            elif command == "find":
                if not args:
                    print("Error: Please provide a search query. Example: find good friends")
                    continue
                
                query_words = [w.lower() for w in args]
                print(f"Searching for pages containing: {', '.join(query_words)}")
                missing, results = find_query(current_index, query_words)

                if missing is None and results is None:
                    print("\nError: The index is empty. Please 'build' or 'load' first.")
                elif missing:
                    print(f"\nSearch failed. The following word(s) were never found during crawling: {', '.join(missing)}")
                elif results:
                    print(f"\nFound {len(results)} page(s) containing: {', '.join(query_words)}")
                    for url, score in results:
                        print(f" - {url} (Total Mentions: {score})")
                else:
                    print(f"\nNo single page was found containing all the words: {', '.join(query_words)}")
            
            elif command in ["exit", "quit"]:
                print("Exiting tool. Goodbye!")
                break

            else:
                print(f"Unknown command: '{command}'. Please use build, load, print, or find.")

        except KeyboardInterrupt:
            # This cleanly handles the user pressing Ctrl+C to force quit
            print("\nForce quitting...")
            break
        except Exception as e:
            # A catch-all so the shell doesn't crash if something goes wrong
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()