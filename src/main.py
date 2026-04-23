import sys
import json
import os
from crawler import crawl_website

INDEX_FILE_PATH = os.path.join("data", "index.json")

def main():
    print("Welcome to the COMP3011 Search Engine Tool")
    print("Available commands: build, load, print <word>, find <query...>, exit")
    
    # This variable will hold the index in memory once loaded
    current_index = None

    # The main shell loop
    while True:
        try:
            # 1. Get input and split it into a list of words
            user_input = input("> ").strip().split()
            
            # If the user just pressed Enter without typing anything
            if not user_input:
                continue
            
            # 2. Separate the command from its arguments
            command = user_input[0].lower()
            args = user_input[1:]

            # 3. Route the command
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
                
                word = args[0].lower() # The brief specifies case-insensitive search
                # print(f"Fetching index data for: '{word}'")
                print("Not implemented")
                

            elif command == "find":
                if not args:
                    print("Error: Please provide a search query. Example: find good friends")
                    continue
                
                query_words = [w.lower() for w in args]
                # print(f"Searching for pages containing: {', '.join(query_words)}")
                print("Not implemented")

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
            # A catch-all so your shell doesn't crash if something goes wrong
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()