import sys
sys.path.append('../../../hscraper/plugins')
sys.path.append('../../../hscraper/plugins/ehen')

import unittest
import ehen_scraper

class Test(unittest.TestCase):


    def setUp(self):
        self.ehen = ehen_scraper.EhenScraper()

    def test_scrap_for_pages(self):
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expecter_urls = ["https://e-hentai.org/g/1087428/b240f1a9ab/",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",]
        
        url_lists = self.ehen.scrap_for_pages()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()