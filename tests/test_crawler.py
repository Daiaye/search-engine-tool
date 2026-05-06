import unittest
from bs4 import BeautifulSoup
from src.crawler import get_all_links

class TestCrawler(unittest.TestCase):

    def test_get_all_links_finds_valid_links(self):
        fake_html = """
        <html>
            <body>
                <a href="/page/2/">Next Page</a>
                <a href="https://wikipedia.org">External Link (Should be ignored!)</a>
                <a href="/author/einstein/">Author Bio</a>
                <!-- Edge Case: Fragments and Queries should be stripped -->
                <a href="/page/2/#top-of-page">Next Page (Fragment)</a>
                <a href="/page/2/?sort=asc">Next Page (Query)</a>
            </body>
        </html>
        """
        soup = BeautifulSoup(fake_html, 'html.parser')
        base_url = "https://quotes.toscrape.com/"

        links = get_all_links(soup, base_url)

        expected_links = [
            "https://quotes.toscrape.com/page/2/",
            "https://quotes.toscrape.com/author/einstein/"
        ]
        
        self.assertCountEqual(links, expected_links)

if __name__ == '__main__':
    unittest.main()