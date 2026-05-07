# COMP3011 Search Engine Tool

## Project Overview and Purpose

This project is a command-line web search engine built for the COMP3011 Web Services and Web Data coursework. It is designed to crawl a target website (`https://quotes.toscrape.com/`), process its HTML content, and build an inverted index.

Beyond standard single-word frequency indexing, this tool features an **Exact Phrase Matching** algorithm. By storing positional data for every parsed word, the search engine can accurately process multi-word queries by verifying that the words appear consecutively on the crawled pages, rather than just returning scattered matches.

## Dependencies

This project requires Python 3.x and relies on two external libraries for HTTP requests and HTML parsing:

* `requests` (for composing HTTP requests and respecting politeness windows)

* `beautifulsoup4` (for parsing HTML and extracting clean text)

You can install the dependencies using the provided `requirements.txt` file.

## Installation and Setup

### 1. Clone the repository
```bash
git clone <https://github.com/Daiaye/search-engine-tool>
cd <search-engine-tool>
```

### 2. Environment setup
Create and activate a virtual environment to isolate project dependencies:

```bash
python -m venv .venv
```

Activate (Windows)
```bash
.\.venv\Scripts\activate
```

Activate (Mac/Linux)
```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage Guide

To start the interactive command-line interface:
```bash
python -m src.main
```

Once the shell is running (>), you can use the following four commands:

`build`: Crawls the target website, respects a 6-second politeness window between requests, builds the inverted index in memory, and saves it to the local file system (data/index.json).

`load`: Loads a previously built index from the file system into memory. You must run this (or `build`) before searching.

`print <word>`: Retrieves and displays the raw indexing statistics (frequency and exact integer positions) for a specific word across all crawled pages. 

Example: `> print nonsense`

`find <query...>`: Searches the index for single or multi-word queries. Single words are ranked by total frequency. Multi-word queries utilise the positional data to perform an Exact Phrase Match, filtering out pages where the words exist but are scattered.

For a single word query: `> find indifference`

For a multi-word query: `> find good friends`

## Testing Instructions

This project utilises Python's built-in `unittest` framework. The testing suite is divided into modular tests for the Crawler, Indexer, and Search logic.

To run all tests:
```bash
python -m unittest discover tests
```

To run a specific module:

For the crawler:
```bash
python -m unittest tests/test_crawler.py
```

For the indexer:
```bash
python -m unittest tests/test_indexer.py
```

For the search:
```bash
python -m unittest tests/test_search.py
```