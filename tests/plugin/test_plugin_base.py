import sys
sys.path.append('../../hscraper/plugin')

import unittest
from bs4 import BeautifulSoup
import hashlib

import plugin_base

class TestClass(plugin_base.PluginBase):
    
    def start(self):
        pass
    
    def scrap_for_images(self):
        pass
    
    def scrap_for_pages(self):
        pass
    
    def scrap_for_posts(self):
        pass

class Test(unittest.TestCase):
    """
    Test Class for plugin base. It tests the methods that do not need to be overriden across plugins.
    """
    def setUp(self):
        self.pb = TestClass()

    def test_get_html(self):
        """
        Tests the request for an html page
        """
        
        response = self.pb.get_request("https://www.webscraper.io/test-sites/tables",1 ,3, 1)
        parser = BeautifulSoup(response["payload"], "html.parser")
        
        tag = parser.find("h1")
        text = "Table playground"
        
        
        self.assertEqual(tag.text, text)
        self.assertEqual(response["retry"], 1)
        self.assertEqual(response["response_code"], 200)
    
      
    def test_get_html_bad_url(self):
        """
        Tests the request for an html page, given a bad url.
        """
        
        response = self.pb.get_request("https://www.websc/es/taasdasd",1 ,1 ,1)        
        
        self.assertEqual(response["payload"], None)
        self.assertEqual(response["retry"], 1)
        self.assertEqual(response["response_code"], 404)
        
    def test_get_html_bad_url_retry(self):
        """
        Tests the request for an html page, given a bad url, must retry 3 times.
        """
        
        response = self.pb.get_request("https://www.websc/es/taasdasd", 1, 3, 1)
        
        self.assertEqual(response["retry"], 3)
        self.assertEqual(response["response_code"], 404)
        self.assertEqual(response["payload"], None)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()