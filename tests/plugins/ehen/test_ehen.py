import sys
sys.path.append('../../../hscraper/plugins')
sys.path.append('../../../hscraper/plugins/ehen')

import re

import unittest
import ehen_scraper

class Test(unittest.TestCase):


    def setUp(self):
        self.ehen = ehen_scraper.EhenScraper()

    def test_scrap_for_pages(self):
        """
        Tests if it can generate the urls of the pages given a starting url
        """
        
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_urls = ["https://e-hentai.org/g/1087428/b240f1a9ab/",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",]
        
        url_lists = self.ehen.scrap_for_pages(given_url, 5, None, None)
        
        for i in range(len(expected_urls)):
            self.assertEqual(url_lists[i], expected_urls[i])
            
    def test_scrap_for_pages_skips_from_2(self):
        """
        Tests if skips pages 1 and 2 from 1 to 5
        """
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_ouput = ["https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",]
        
        out = self.ehen.scrap_for_pages(given_url, 5, skip_from=2)
        for i in range(3):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_scrap_for_pages_skip_from_2_to_3(self):
        """
        Tests if skips pages 1 and 2 to 5, from 1 to 5
        """
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_ouput = ["https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",]
            
        out = self.ehen.scrap_for_pages(given_url, 5, skip_from=1, skip_to=3)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_validate_url(self):
        """
        Tests if it validates urls using a regular expression
        """
        
        given_urls = ["https://e-hentai.org/g/1087428/b240f1a9ab/",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",
                      ]
        bad_url = "wrong!"
        
        for url in given_urls:
            self.assertTrue(self.ehen.validate_url(url))
        
        self.assertFalse(self.ehen.validate_url(bad_url))
        
    def test_scrap_for_posts(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        response = self.ehen.scrap_for_posts(url, 1, 1, 1)
        
        pat = re.compile(r'https:\/\/e-hentai\.org\/s\/[\S]{10}\/[\d]+-[\d]+')
        for post in response:
            self.assertTrue(pat.match(post))
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()