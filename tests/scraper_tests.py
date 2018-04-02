'''
Created on 30/03/2018

@author: David
'''
import unittest
from hscrap.scraper import Scraper
from hscrap.web_retriever import WebRetriever
from urllib.request import Request, urlopen
import time
import random

class Test(unittest.TestCase):


    def test_module_exists(self):
        scr = Scraper()
        
    def test_scrap_ehentai(self):
        """
        -Donwloads an html page from ehentai.
        -Then, search for gdt div.
        -Then extract every "a" tag href attribute inside it.
        -Returns a list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://e-hentai.org/g/1178602/df79f996bc/"
        data = WebRetriever().retrieve_ehentai(url,pages)
        
        links = Scraper().scrap_ehentai(data[0])
        
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        
    def test_scrap_danbooru(self):
        """
        -Donwloads an html page from danbooru.
        -Then, search for posts div.
        -Then extract every "a" tag href attribute inside it.
        -Returns a list of every link to the individual image posts.
        """
        
        pages = 1
        url = "http://danbooru.donmai.us/posts?tags=touhou"
        data = WebRetriever().retrieve_danbooru(url,pages)
        
        links = Scraper().scrap_danbooru(data[0])
        
        
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        
    def test_scrap_r34(self):
        """
        -Donwloads an html page from r34.xxx.
        -Then, search for div which CLASS is content.
        -Then extract every "a" tag href attribute inside it.
        -Returns a list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=dandon_fuga"
        data = WebRetriever().retrieve_r34(url,pages)
        
        links = Scraper().scrap_r34(data[0])
        
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        
    def test_scrap_hitomi_la(self):
        """
        -Donwloads an html page from hitomi.la.
        -Then, search for ul which CLASS is thumbnail-list.
        -Then extract every "a" tag href attribute inside it.
        -Returns a list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://hitomi.la/galleries/1198858.html"
        data = WebRetriever().retrieve_hitomi_la(url,pages)
        
        links = Scraper().scrap_hitomi_la(data[0])
        
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links)))


        
    def _pull_html_for_acceptance(self,url):
        """Tries to pull an url from the web, if succeeds, returns true."""
        try:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            html = data.decode('utf-8')
            time.sleep(1)
            return True
        except:
            return False

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_module_exists']
    unittest.main()