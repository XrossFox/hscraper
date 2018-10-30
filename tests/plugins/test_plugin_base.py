import sys
import os
sys.path.append('../../hscraper/plugins')

import unittest
from bs4 import BeautifulSoup

import plugin_base

class TestClass(plugin_base.PluginBase):
    
    def start(self):
        pass
    
    def validate_url(self, url):
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
        
    def test_create_dir(self):
        """
        Tests the creation of a directory given a path
        """
        
        self.pb.create_dir(path="test_directory")
        
        self.assertTrue(os.path.exists("test_directory"))
        
    def test_create_invalid_char_dir(self):
        """
        Tests the creation of a directory given an path with invalid characters
        """
        
        self.pb.create_dir(path="?test_directory2:")
        
        self.assertTrue(os.path.exists("test_directory2"))
        
    def test_write_to_image(self):
        resp = self.pb.get_request("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Facebook_New_Logo_%282015%29.svg/1200px-Facebook_New_Logo_%282015%29.svg.png",
                            wait=1, retry=1, wait_retry=1)
        
        self.pb.write_to(path="", name="le_test.png", payload=bytes(resp['payload']))
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()