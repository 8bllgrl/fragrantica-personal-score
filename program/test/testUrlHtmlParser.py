import unittest

from program.testableHtmlParser import scrape_page


class TestScraper(unittest.TestCase):
    def test_scrape_page(self):
        # Example URL of a perfume page on Fragrantica (replace with a real test URL)
        test_url = "https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Clean-Suede-82999.html"

        perfume_details = scrape_page(test_url)

        self.assertEqual(perfume_details.url, "https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Clean-Suede-82999.html")
        self.assertEqual(perfume_details.perfume_name, "Clean Suede Etat Libre d'Orangefor women and men")
        self.assertGreater(len(perfume_details.accords), 0, "Accords should not be empty")
        accord_names = [accord.name for accord in perfume_details.accords]
        self.assertIn("leather", accord_names)
        self.assertIn("powdery", accord_names)
        self.assertGreater(len(perfume_details.notes), 0, "Notes should not be empty")
        note_names = [note.name for note in perfume_details.notes]
        self.assertIn("Suede", note_names)
        self.assertIn("Vanilla", note_names)

    def test_scrape_page_without_note_categories(self):
        test_url = "https://www.fragrantica.com/perfume/Fine-ry/Without-A-Trace-91430.html"
        # no distinction between top,middle,base notes. but i want it to recognize them anyways.
        perfume_details = scrape_page(test_url)

        self.assertEqual(perfume_details.url, "https://www.fragrantica.com/perfume/Fine-ry/Without-A-Trace-91430.html")
        self.assertGreater(len(perfume_details.notes), 0, "Notes should not be empty")
        note_names = [note.name for note in perfume_details.notes]
        self.assertIn("Musk", note_names)
        self.assertIn("Suede", note_names)
        self.assertIn("Neroli", note_names)
        self.assertIn("Cedarwood", note_names)




if __name__ == '__main__':
    unittest.main()
