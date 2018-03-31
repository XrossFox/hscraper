'''
Created on 30/03/2018

@author: David
'''
import unittest
import os
from hscrap.scraper import Scraper
from hscrap.web_retriever import WebRetriever


class Test(unittest.TestCase):


    def test_module_exists(self):
        scr = Scraper()
        
    def test_scrap_and_retrieve_ehentai(self):
        """
        -Donwloads an html page from ehentai.
        -Then, search for gdt div.
        -Then extract every "a" tag href attribute inside it.
        -Returns a list of every link.
        -This gets us only the links to the posts of each image, further scrapping
        is stll needed to retrieve the image url, which is the one we want.
        -Download the image from da internetz to the specified path.
        """
        """
        scr = Scraper()
        
        pages = 1
        url = "https://e-hentai.org/g/1178602/df79f996bc/"
        data = WebRetriever().retrieve_ehentai(url,pages)
        o_path = os.path.dirname(__file__)+"\\"
        
        Scraper().scrap_ehentai(data[0],o_path)
        
        self.assertTrue(os.path.isdir(o_path+"\\"+"[nonsummerjack (non)] Arabian Nights"+"\\000.jpg"))
        self.assertTrue(os.path.isdir(o_path+"\\"+"[nonsummerjack (non)] Arabian Nights"+"\\001.jpg"))
        self.assertTrue(os.path.isdir(o_path+"\\"+"[nonsummerjack (non)] Arabian Nights"+"\\002.jpg"))
        self.assertTrue(os.path.isdir(o_path+"\\"+"[nonsummerjack (non)] Arabian Nights"+"\\003.jpg"))
        """
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_module_exists']
    unittest.main()