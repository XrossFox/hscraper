'''
Created on 05/03/2018

@author: David
'''
import unittest
from hscrap import global_vars
from hscrap.web_retriever import WebRetriever
class Test(unittest.TestCase):


    def test_init_throws_except_if_not_send_global_varaibles_instance(self):
        """Checks that if sent a parameter that is not an instance of GlobalVars, an
        exception is raised"""
        
        with self.assertRaises(Exception):
            web = WebRetriever("web_retriever")

    def test_retrieve_from_ehentai_2_pages(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 2 pages to retrieve"""
        glob = global_vars.GlobalVars()
        glob.set_no_pages(2)
        glob.set_url("https://e-hentai.org/g/1178602/df79f996bc/")
        data = WebRetriever(glob).retrieve_ehentai()
        self.assertTrue(isinstance(data, list))
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[0])
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[1])
    
    def test_retrieve_from_ehentai_1_page(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 1 page to retrieve"""
        glob = global_vars.GlobalVars()
        glob.set_no_pages(1)
        glob.set_url("https://e-hentai.org/g/1178602/df79f996bc/")
        data = WebRetriever(glob).retrieve_ehentai()
        self.assertTrue(isinstance(data, list))
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[0])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()