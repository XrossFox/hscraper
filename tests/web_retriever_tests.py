'''
Created on 05/03/2018

@author: David
'''
import unittest
from hscrap.web_retriever import WebRetriever
import os
class Test(unittest.TestCase):

    #--------------------------------
    def test_retrieve_from_ehentai_2_pages(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 2 pages to retrieve"""
        pages = 2
        url = "https://e-hentai.org/g/1178602/df79f996bc/"
        data = WebRetriever().retrieve_ehentai(url,pages)
        self.assertTrue(isinstance(data, list))
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[0])
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[1])
    
    def test_retrieve_from_ehentai_1_page(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 1 page to retrieve"""
        pages = 1
        url = "https://e-hentai.org/g/1178602/df79f996bc/"
        data = WebRetriever().retrieve_ehentai(url,pages)
        self.assertTrue(isinstance(data, list))
        self.assertIn("[nonsummerjack (non)] Arabian Nights - E-Hentai Galleries", data[0])
        
    #-------------------------------
    
    def test_retrieve_from_danbooru_2_pages(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 2 pages to retrieve"""
        pages = 2
        url = "http://danbooru.donmai.us/posts?tags=touhou"
        data = WebRetriever().retrieve_danbooru(url,pages)
        self.assertTrue(isinstance(data, list))
        #Tests for title tag
        self.assertIn("touhou - Danbooru", data[0])
        self.assertIn("touhou - Danbooru", data[1])
    
    def test_retrieve_from_danbooru_1_page(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 1 page to retrieve"""
        pages = 1
        url = "http://danbooru.donmai.us/posts?tags=touhou"
        data = WebRetriever().retrieve_danbooru(url,pages)
        self.assertTrue(isinstance(data, list))
        self.assertIn("touhou - Danbooru", data[0])
        
    #-------------------------------
    
    def test_retrieve_from_r34_2_pages(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 2 pages to retrieve"""
        pages = 2
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=dandon_fuga+"
        data = WebRetriever().retrieve_r34(url,pages)
        self.assertTrue(isinstance(data, list))
        #Tests for title tag
        self.assertIn("Rule 34  / dandon_fuga ", data[0])
        self.assertIn("Rule 34  / dandon_fuga ", data[1])
    
    def test_retrieve_from_r34_1_page(self):
        """Tests that it returns a list of the pages, with the HTML code of each page. Test with 1 page to retrieve"""
        pages = 1
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=dandon_fuga+"
        data = WebRetriever().retrieve_r34(url,pages)
        self.assertTrue(isinstance(data, list))
        self.assertIn("Rule 34  / dandon_fuga ", data[0])
        
    #-------------------------------

    def test_retrieve_from_hitomi(self):
        """Tests that it returns a list of the pages, with the HTML code of each page."""
        url = "https://hitomi.la/reader/1198858.html#5"
        data = WebRetriever().retrieve_hitomi_la(url)
        self.assertTrue(isinstance(data, list))
        #Tests for title tag
        self.assertIn("Hitozuma Club | Hitomi.la", data[0])
           
    def test_retrieve_post(self):
        """Retrieves an image post fron da internetz"""
        post_url = "https://e-hentai.org/s/550514aad7/1178602-39"
        web = WebRetriever()
        web.retrieve_web_page(post_url)
        
    def test_retrieve_image(self):
        img_list = ["https://0a.hitomi.la/galleries/1198858/009.jpg","https://0a.hitomi.la/galleries/1198858/008.jpg",
                    "https://rule34.xxx//images/2351/5b6eb0cd48d183104e6a9636dde886b0.jpeg",
                    "https://rule34.xxx//samples/1183/sample_12a523c3f02f7b8cbf87292ff99132cd.jpg",
                    "https://danbooru.donmai.us/data/sample/__yorigami_shion_touhou_drawn_by_misha_hoongju__sample-b5d5bea079a3f08fea80ed84f028ec42.jpg",
                    "https://danbooru.donmai.us/data/__inubashiri_momiji_touhou_drawn_by_leon_mikiri_hassha__de0d58fa4cd64df1a18f48a813c0a950.jpg",
                    "http://54.36.151.63:10069/h/2a50fb59be233a91827a18baf95de4e6ec39f52e-221826-770-916-jpg/keystamp=1523062800-09e923d5a4;fileindex=60033795;xres=org/0_Cover.jpg",
                    "http://204.44.102.254:8900/h/c2ac98f32e2f529c85de8fa00b2d5f626363e9a5-81330-960-720-jpg/keystamp=1523063100-fe093846e4;fileindex=40251965;xres=2400/1f496e105639dfbbba03db6f06407b59.jpg"
                    ]
        
        web = WebRetriever()
        path = os.path.dirname(__file__)
        for img_url in img_list:
            web.retrieve_image(img_url,path)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()