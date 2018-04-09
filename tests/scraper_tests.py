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
        -Returns a touple of galleryname / list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://e-hentai.org/g/1178602/df79f996bc/"
        data = WebRetriever().retrieve_ehentai(url,pages)
        
        links = Scraper().scrap_ehentai(data[0])
        self.assertTrue(links[0] in "[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries")
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        
    def test_scrap_danbooru(self):
        """
        -Donwloads an html page from danbooru.
        -Then, search for posts div.
        -Then extract every "a" tag href attribute inside it.
        -Returns a touple of galleryname / list of every link to the individual image posts.
        """
        
        pages = 1
        url = "http://danbooru.donmai.us/posts?tags=touhou"
        data = WebRetriever().retrieve_danbooru(url,pages)
        
        links = Scraper().scrap_danbooru(data[0])
        print(links[0])
        self.assertTrue(links[0].strip() in "touhou - Danbooru")
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
   
    def test_scrap_r34(self):
        """
        -Donwloads an html page from r34.xxx.
        -Then, search for div which CLASS is content.
        -Then extract every "a" tag href attribute inside it.
        -Returns a touple of galleryname / list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=dandon_fuga"
        data = WebRetriever().retrieve_r34(url,pages)
        
        links = Scraper().scrap_r34(data[0])
        self.assertTrue(links[0] in "Rule 34  / dandon_fuga")
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
    #---
    def test_scrap_post_hitomi_la(self):
        """
        -Donwloads an html page from hitomi.la READER.
        -Then, search for ul which CLASS is thumbnail-list.
        -Then extract every "a" tag href attribute inside it.
        -Returns a touple of galleryname / list of every link to the individual image posts.
        """
        
        pages = 1
        url = "https://hitomi.la/reader/1198858.html#5"
        data = WebRetriever().retrieve_hitomi_la(url,pages)
        
        links = Scraper().scrap_post_hitomi_la(data[0])
        self.assertTrue(links[0] in "Hitozuma Club | Hitomi.la")
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
        self.assertTrue(self._pull_html_for_acceptance(random.choice(links[1])))
    #---
    def test_scrap_post_ehentai(self):
        """ - scrap_post must receive an url to a post with an image.
            - then it must look for the url of the image, img tag with id=img (duh!).
            - return the url collected from the src attribute.
        """
        post_url = "https://e-hentai.org/s/550514aad7/1178602-39"
        img_url = Scraper().scrap_post_ehentai(post_url)
        
        img = "038.jpg"
        self.assertEqual(img, img_url.split("/")[-1])
    
        
    def test_scrap_post_danbooru(self):
        """ - scrap_post must receive an url to a post with an image.
            - then it must look for the url of the image, img tag with id=image (double duh!).
            - return the url collected from the src attribute.
        """
        post_url = "http://danbooru.donmai.us/posts/3074486"
        img_url = Scraper().scrap_post_danbooru(post_url)
        
        img = "__inubashiri_momiji_touhou_drawn_by_leon_mikiri_hassha__de0d58fa4cd64df1a18f48a813c0a950.jpg"
        self.assertEqual(img, img_url.split("/")[-1])
    
    
    def test_scrap_post_r34(self):
        """ - scrap_post must receive an url to a post with an image.
            - then it must look for the url of the image, img tag with id=image (triple duh!).
            - return the url collected from the src attribute.
        """
        post_url = "https://rule34.xxx/index.php?page=post&s=view&id=2710033"
        img_url = Scraper().scrap_post_r34(post_url)
        
        img = "sample_12a523c3f02f7b8cbf87292ff99132cd.jpg?2710033"
        self.assertEqual(img, img_url.split("/")[-1])
    

    def _pull_html_for_acceptance(self,url):
        """Tries to pull an url from the web, if succeeds, returns true."""
        try:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            time.sleep(1)
            return True
        except:
            return False

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_module_exists']
    unittest.main()