import unittest
from bs4 import BeautifulSoup
from src.indexer import clean_text, index_page_content

class TestIndexer(unittest.TestCase):

    def test_clean_text_removes_punctuation_and_lowercases(self):
        fake_html = "<div><p>Hello, World!</p> <span>Good   friends.</span></div>"
        soup = BeautifulSoup(fake_html, 'html.parser')
        
        words = clean_text(soup)
        
        expected_words = ['hello', 'world', 'good', 'friends']
        self.assertEqual(words, expected_words)

    def test_clean_text_removes_noise_tags(self):
        fake_html = """
        <html>
            <style>.hidden { display: none; }</style>
            <script>let count = 5; console.log(count);</script>
            <p>Only keep this text.</p>
        </html>
        """
        soup = BeautifulSoup(fake_html, 'html.parser')
        
        words = clean_text(soup)
        
        expected_words = ['only', 'keep', 'this', 'text']
        self.assertEqual(words, expected_words)

    def test_index_page_content_creates_new_entries(self):
        fake_html = "<p>apple apple banana</p>"
        soup = BeautifulSoup(fake_html, 'html.parser')
        url = "https://quotes.toscrape.com/page/1/"
        empty_index = {}
        
        updated_index = index_page_content(soup, url, empty_index)
        
        self.assertIn("apple", updated_index)
        self.assertIn("banana", updated_index)
        
        self.assertEqual(updated_index["apple"][url]["frequency"], 2)
        self.assertEqual(updated_index["apple"][url]["positions"], [0, 1])
        
        self.assertEqual(updated_index["banana"][url]["frequency"], 1)
        self.assertEqual(updated_index["banana"][url]["positions"], [2])

    def test_index_page_content_updates_existing_index(self):
        # Start with an index that ALREADY has "apple" from page 1
        existing_index = {
            "apple": {
                "https://quotes.toscrape.com/page/1/": {"frequency": 1, "positions": [0]}
            }
        }
        
        fake_html = "<p>apple</p>"
        soup = BeautifulSoup(fake_html, 'html.parser')
        new_url = "https://quotes.toscrape.com/page/2/"
        
        updated_index = index_page_content(soup, new_url, existing_index)
        
        self.assertIn("https://quotes.toscrape.com/page/1/", updated_index["apple"])
        self.assertIn("https://quotes.toscrape.com/page/2/", updated_index["apple"])
        
        self.assertEqual(updated_index["apple"][new_url]["frequency"], 1)

if __name__ == '__main__':
    unittest.main()