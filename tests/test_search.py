import unittest
from src.search import get_missing_words, get_matching_urls, rank_results, find_query, get_word_statistics

class TestSearch(unittest.TestCase):
    
    def setUp(self):
        """Creates a fake index before each test to simulate crawled data."""
        self.fake_index = {
            "good": {
                "https://page1.com/": {"frequency": 1, "positions": [0]},
                "https://page2.com/": {"frequency": 3, "positions": [5, 10, 15]}
            },
            "friends": {
                "https://page2.com/": {"frequency": 1, "positions": [6]}
            },
            "miracle": {
                "https://page3.com/": {"frequency": 5, "positions": [1, 2, 3, 4, 5]}
            }
        }

    # --- HELPER FUNCTION TESTS ---

    def test_get_missing_words(self):
        missing = get_missing_words(self.fake_index, ["good", "aliens"])
        self.assertEqual(missing, ["aliens"])

    def test_get_matching_urls_intersection(self):
        matches = get_matching_urls(self.fake_index, ["good", "friends"])
        self.assertEqual(matches, {"https://page2.com/"})

    def test_get_matching_urls_empty_intersection(self):
        matches = get_matching_urls(self.fake_index, ["good", "miracle"])
        self.assertEqual(matches, set())

    def test_rank_results_sorting_and_scoring(self):
        matching_urls = {"https://page1.com/", "https://page2.com/"}
        ranked = rank_results(self.fake_index, matching_urls, ["good"])
        
        expected_ranking = [
            ("https://page2.com/", 3),
            ("https://page1.com/", 1)
        ]
        self.assertEqual(ranked, expected_ranking)

    # --- MAIN ORCHESTRATOR TESTS ---

    def test_find_query_success(self):
        # Action: Run the full search command
        missing, results = find_query(self.fake_index, ["good", "friends"])
        
        # Assert: No missing words, and it returns Page 2 with a score of 4
        self.assertEqual(missing, [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("https://page2.com/", 4))

    def test_find_query_missing_word(self):
        # Action: Run a search with a non-existent word
        missing, results = find_query(self.fake_index, ["good", "aliens"])
        
        # Assert: It returns "aliens" as missing, and an empty results list
        self.assertEqual(missing, ["aliens"])
        self.assertEqual(results, [])

    def test_get_word_statistics_success(self):
        # Action: Request stats for "good"
        stats = get_word_statistics(self.fake_index, "good")
        
        # Assert: It should return a list with 2 items (page 1 and page 2)
        self.assertEqual(len(stats), 2)

if __name__ == '__main__':
    unittest.main()