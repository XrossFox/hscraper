'''
Created on 21/02/2018

@author: XrossFox
'''
import unittest
import os
from hscrap import h_core

class Test(unittest.TestCase):
    """Test Class for h_core module"""   
    def test_url_only_accepts_ehen_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://e-hentai.org/"
        i._check_url_domain(url)
        
    def test_url_only_accepts_dan_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "http://danbooru.donmai.us"
        i._check_url_domain(url)
        
    def test_url_only_accepts_r34_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://rule34.xxx/"
        i._check_url_domain(url)
        
    def test_url_only_accepts_hito_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://hitomi.la/"
        i._check_url_domain(url)   
             
    def test_url_invalid_domain(self):
        with self.assertRaises(Exception):
            """Tests if sent link is a supported website"""
            i = h_core.HCore()
            url = "https://www.google.com"
            with self.assertRaises(Exception):
                i._check_url_domain(url)
            
    def test_input_non_int_pages_exception(self):
        """Tests for integer only pages. Raises non str exception"""
        with self.assertRaises(Exception):
            i = h_core.HCore()
            with self.assertRaises(Exception):
                i._check_for_pages("im an str")
                i._check_for_pages(-1)
            
    def test_create_dir_creates_dir(self):
        """Test for creating directories"""
        path = os.path.dirname(__file__)+"\\"
        name = "test"
        dir = h_core.HCore()
        dir.create_output_dir(path,name)
        self.assertTrue(os.path.isdir(path+name))
        os.rmdir(path+name)
    
 
    def test_user_input_ehentai(self):
        """Should be given a gallery url and download the images in it"""
        galley_url = "https://e-hentai.org/g/1208334/b6d82f86d5/"
        pages = 1
        wait = 2
        core = h_core.HCore()
        core.user_input(galley_url, pages, os.path.dirname(__file__), wait)
    
    def test_danbooru(self):
        galley_url = "https://danbooru.donmai.us/posts?tags=tatsuwo"
        pages = 1
        wait = 1
        core = h_core.HCore()
        core.user_input(galley_url, pages, os.path.dirname(__file__), wait)
     
    def test_rule34(self):
        galley_url = "https://rule34.xxx/index.php?page=post&s=list&tags=sakimichan"
        pages = 1
        wait = 1
        core = h_core.HCore()
        core.user_input(galley_url, pages, os.path.dirname(__file__), wait)  
    
    def test_hitomi(self):
        galley_url = "https://hitomi.la/reader/960714.html#1"
        pages = 1
        wait = 1
        core = h_core.HCore()
        core.user_input(galley_url, pages, os.path.dirname(__file__), wait)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()