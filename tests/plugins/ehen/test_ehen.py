import sys
sys.path.append('../../../hscraper/plugins')
sys.path.append('../../../hscraper/plugins/ehen')

import unittest
import ehen_scraper

class Test(unittest.TestCase):


    def setUp(self):
        self.ehen = ehen_scraper.EhenScraper()

    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()