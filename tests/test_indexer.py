import unittest
from bs4 import BeautifulSoup
from src.indexer import clean_text, index_page_content

class TestIndexer(unittest.TestCase):

    def test_clean_text_removes_punctuation_and_lowercases(self):
        # Create a fake HTML snippet with edge cases
        fake_html = "<div><p>Hello, World!</p> <span>Good   friends.</span></div>"
        soup = BeautifulSoup(fake_html, 'html.parser')
        
        words = clean_text(soup)
        
        # Should be lowercase, no punctuation, and the multiple spaces ignored
        expected_words = ['hello', 'world', 'good', 'friends']
        self.assertEqual(words, expected_words)

    def test_index_page_content_creates_new_entries(self):
        fake_html = "<p>apple apple banana</p>"
        soup = BeautifulSoup(fake_html, 'html.parser')
        url = "https://quotes.toscrape.com/page/1/"
        empty_index = {}
        
        updated_index = index_page_content(soup, url, empty_index)
        
        # Check dictionary structure
        self.assertIn("apple", updated_index)
        self.assertIn("banana", updated_index)
        
        # Apple appears twice: positions 0 and 1
        self.assertEqual(updated_index["apple"][url]["frequency"], 2)
        self.assertEqual(updated_index["apple"][url]["positions"], [0, 1])
        
        # Banana appears once: position 2
        self.assertEqual(updated_index["banana"][url]["frequency"], 1)
        self.assertEqual(updated_index["banana"][url]["positions"], [2])

    def test_index_page_content_updates_existing_index(self):
        # Start with an index that ALREADY has "apple" from page 1
        existing_index = {
            "apple": {
                "https://quotes.toscrape.com/page/1/": {"frequency": 1, "positions": [0]}
            }
        }
        
        fake_html = "<p>apple</p>" # We find apple again on page 2!
        soup = BeautifulSoup(fake_html, 'html.parser')
        new_url = "https://quotes.toscrape.com/page/2/"
        
        updated_index = index_page_content(soup, new_url, existing_index)
        
        # Assert: "apple" should now have TWO URLs listed under it
        self.assertIn("https://quotes.toscrape.com/page/1/", updated_index["apple"])
        self.assertIn("https://quotes.toscrape.com/page/2/", updated_index["apple"])
        
        # Check that the new URL recorded the frequency correctly
        self.assertEqual(updated_index["apple"][new_url]["frequency"], 1)

if __name__ == '__main__':
    unittest.main()