import unittest
from bs4 import BeautifulSoup
from src.crawler import get_all_links

class TestCrawler(unittest.TestCase):

    def test_get_all_links_finds_valid_links(self):
        # 1. Create fake HTML instead of downloading a real page
        fake_html = """
        <html>
            <body>
                <a href="/page/2/">Next Page</a>
                <a href="https://wikipedia.org">External Link (Should be ignored!)</a>
                <a href="/author/einstein/">Author Bio</a>
            </body>
        </html>
        """
        soup = BeautifulSoup(fake_html, 'html.parser')
        base_url = "https://quotes.toscrape.com/"

        # 2. Run worker function
        links = get_all_links(soup, base_url)

        # 3. Check (assert) if it did exactly what we expect
        # It should ignore Wikipedia, and convert the other two to absolute URLs.
        expected_links = [
            "https://quotes.toscrape.com/page/2/",
            "https://quotes.toscrape.com/author/einstein/"
        ]
        
        self.assertEqual(links, expected_links)

if __name__ == '__main__':
    unittest.main()