'''
Created on 21/02/2018

@author: XrossFox
'''
import unittest
import os
from hscrap import h_core

class Test(unittest.TestCase):
    """Test Class for h_core module"""
    
    def test_input_set_global_vars(self):
        """
        Tests if input_user sets the global variables
        """
        i = h_core.HCore()
        url = "https://e-hentai.org/"
        no_pages = 1
        global_reference = i.user_input(url, no_pages)
        self.assertEqual(global_reference.get_url(), url)
        self.assertEqual(global_reference.get_no_pages(), no_pages)
        
    def test_input_set_global_vars_plus_default_path(self):
        """
        Tests if input_user sets the global variables
        """
        i = h_core.HCore()
        url = "https://e-hentai.org/"
        no_pages = 1
        global_reference = i.user_input(url, no_pages)
        self.assertEqual(global_reference.get_url(), url)
        self.assertEqual(global_reference.get_no_pages(), no_pages)
        
    def test_url_only_accepts_ehen_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://e-hentai.org/"
        no_pages = 1
        i.user_input(url, no_pages)
        
    def test_url_only_accepts_dan_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "http://danbooru.donmai.us"
        no_pages = 1
        i.user_input(url, no_pages)
        
    def test_url_only_accepts_r34_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://rule34.xxx/"
        no_pages = 1
        i.user_input(url, no_pages)
        
    def test_url_only_accepts_hito_domain(self):
        """Tests if sent link is a supported website"""
        i = h_core.HCore()
        url = "https://hitomi.la/"
        no_pages = 1
        i.user_input(url, no_pages)   
             
    def test_url_invalid_domain(self):
        with self.assertRaises(Exception):
            """Tests if sent link is a supported website"""
            i = h_core.HCore()
            url = "https://www.google.com"
            no_pages = 1
            i.user_input(url, no_pages)
            
    def test_input_non_int_pages_exception(self):
        """Tests for integer only pages. Raises non str exception"""
        with self.assertRaises(Exception):
            i = h_core.HCore()
            url = "https://e-hentai.org/"
            no_pages = "im an str"
            i.user_input(url, no_pages)
            
    def test_create_dir_creates_dir(self):
        """Test for creating directories"""
        path = os.path.dirname(__file__)+"\\"
        name = "test"
        dir = h_core.HCore()
        dir.create_output_dir(path,name)
        self.assertTrue(os.path.isdir(path+name))
        os.rmdir(path+name)
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()