import unittest
from src.search import (
    get_missing_words, 
    get_matching_urls, 
    rank_results, 
    find_query, 
    get_word_statistics
)

class TestSearch(unittest.TestCase):
    
    def setUp(self):
        """Creates a fake index before each test to simulate crawled data."""
        self.fake_index = {
            "good": {
                "https://page1.com/": {"frequency": 1, "positions": [0]},
                "https://page2.com/": {"frequency": 3, "positions": [5, 10, 15]},
                "https://page4.com/": {"frequency": 2, "positions": [2, 20]}
            },
            "friends": {
                "https://page2.com/": {"frequency": 1, "positions": [6]},
                "https://page4.com/": {"frequency": 2, "positions": [10, 30]}
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
        self.assertEqual(matches, {"https://page2.com/", "https://page4.com/"})

    def test_get_matching_urls_empty_intersection(self):
        matches = get_matching_urls(self.fake_index, ["good", "miracle"])
        self.assertEqual(matches, set())

    def test_rank_results_sorting_and_scoring(self):
        matching_urls = {"https://page1.com/", "https://page2.com/"}
        # Single word search uses standard frequency (3 vs 1)
        ranked = rank_results(self.fake_index, matching_urls, ["good"])
        
        expected_ranking = [
            ("https://page2.com/", 3),
            ("https://page1.com/", 1)
        ]
        self.assertEqual(ranked, expected_ranking)

    def test_rank_results_exact_phrase(self):
        matching_urls = {"https://page2.com/"}
        # Multi-word search uses exact phrase frequency
        ranked = rank_results(self.fake_index, matching_urls, ["good", "friends"])
        
        # 'good' is at 5, 'friends' is at 6. Phrase frequency is 1.
        self.assertEqual(ranked, [("https://page2.com/", 1)])

    def test_rank_results_non_consecutive_phrase(self):
        matching_urls = {"https://page4.com/"}
        # Words exist on page 4, but are scattered (positions [2, 20] and [10, 30])
        ranked = rank_results(self.fake_index, matching_urls, ["good", "friends"])
        
        # Since they never appear consecutively, it should be filtered out
        self.assertEqual(ranked, [])

    # --- MAIN ORCHESTRATOR TESTS ---

    def test_find_query_success(self):
        # Action: Run the full search command
        missing, results = find_query(self.fake_index, ["good", "friends"])
        
        # Assert: No missing words, and it returns Page 2 with a score of 1 (exact phrase match)
        self.assertEqual(missing, [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("https://page2.com/", 1))

    def test_find_query_missing_word(self):
        # Action: Run a search with a non-existent word
        missing, results = find_query(self.fake_index, ["good", "aliens"])
        
        # Assert: It returns "aliens" as missing, and an empty results list
        self.assertEqual(missing, ["aliens"])
        self.assertEqual(results, [])

    def test_get_word_statistics_success(self):
        # Action: Request stats for "good"
        stats = get_word_statistics(self.fake_index, "good")
        
        # Assert: It should return a list with 3 items (page 1, page 2, and page 4)
        self.assertEqual(len(stats), 3)

if __name__ == '__main__':
    unittest.main()