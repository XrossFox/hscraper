import sys
sys.path.append('../../../hscraper/plugins')
sys.path.append('../../../hscraper/plugins/ehen')

import re

import unittest
import ehen_scraper

class Test(unittest.TestCase):


    def setUp(self):
        self.ehen = ehen_scraper.EhenScraper()

    def test_scrap_for_pages(self):
        """
        Tests if it can generate the urls of the pages given a starting url
        """
        
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_urls = ["https://e-hentai.org/g/1087428/b240f1a9ab/",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",]
        
        url_lists = self.ehen.scrap_for_pages(given_url, 5, None)
        
        for i in range(len(expected_urls)):
            self.assertEqual(url_lists[i], expected_urls[i])
            
    def test_scrap_for_pages_skips_from_2(self):
        """
        Tests if skips pages 1 and 2 from 1 to 5
        """
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_ouput = ["https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",]
        
        out = self.ehen.scrap_for_pages(given_url, 5, skip_from=2)
        for i in range(3):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_scrap_for_pages_skip_from_2_to_3(self):
        """
        Tests if skips pages 1 and 2 to 5, from 1 to 5
        """
        given_url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        expected_ouput = ["https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                         "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",]
            
        out = self.ehen.scrap_for_pages(given_url, 3, skip_from=1)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_validate_url(self):
        """
        Tests if it validates urls using a regular expression
        """
        
        given_urls = ["https://e-hentai.org/g/1087428/b240f1a9ab/",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=1",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=2",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=3",
                      "https://e-hentai.org/g/1087428/b240f1a9ab/?p=4",
                      ]
        bad_url = "wrong!"
        
        for url in given_urls:
            self.assertTrue(self.ehen.validate_url(url))
        
        self.assertFalse(self.ehen.validate_url(bad_url))
        
    def test_scrap_for_posts(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        
        response = self.ehen.scrap_for_posts(url, 1, 1, 1)
        
        pat = re.compile(r'https:\/\/e-hentai\.org\/s\/[\S]{10}\/[\d]+-[\d]+')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_none(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = None
        
        response = self.ehen.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
    
    def test_scrap_for_posts_timed_out_or_not_found(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = "invalid_url"
        
        response = self.ehen.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_posts_cookie(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression. This particular
        page has a content warning and needs a cookie to access to it.
        """
        
        url = "https://e-hentai.org/g/1263299/a42ce2eb95/"
        
        response = self.ehen.scrap_for_posts(url, 1, 1, 1)
        
        pat = re.compile(r'https:\/\/e-hentai\.org\/s\/[\S]{10}\/[\d]+-[\d]+')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_images(self):
        """
        Tests scrap_for_images for the links it returns
        """
        
        post_test_links = [
            "https://e-hentai.org/s/1a08f5de00/1084306-2",
            "https://e-hentai.org/s/b94e838b59/1084306-3",
            "https://e-hentai.org/s/5bf407a7f1/1084306-4",
            "https://e-hentai.org/s/bbc0a8c0d7/1084306-5",
            "https://e-hentai.org/s/b241919d8d/1084306-6",
            ]
        
        expected_output = [
            ('1084306-2',"http://23.92.78.158:6112/h/efc92aaf5535f5c85a87998d89ede99e5f347809-168478-1200-1798-jpg/keystamp=1541196000-3ce6e7ac0d;fileindex=51789718;xres=2400/001.jpg",'jpg'),
            ('1084306-3',"http://209.141.35.151:60120/h/53bf97dd05b0dc032d1b0ac97cf55c7a4720d0e1-156204-1200-1798-jpg/keystamp=1541196000-f4fc58709a;fileindex=53687877;xres=2400/002.jpg","jpg"),
            ('1084306-4',"http://104.129.16.91:33333/h/17d1035d9bc93b8b72bd1fd3a3d731184bb44eea-130040-1200-1798-jpg/keystamp=1541196000-7f3a514392;fileindex=53687878;xres=2400/003.jpg",'jpg'),
            ('1084306-5',"http://199.19.225.182:41088/h/1f0ccbd56f8ca1a6d9d0fc720725d62ba4718306-124584-1200-1798-jpg/keystamp=1541196000-23d8564389;fileindex=53687879;xres=2400/004.jpg",'jpg'),
            ('1084306-6',"http://98.116.77.140:2688/h/300e9d9ea4afcef891e032c4bad09c255d0b2731-65986-1280-855-jpg/keystamp=1541196000-d2d727b472;fileindex=53687880;xres=1280/005.jpg",'jpg'),
            ]
        
        list_of_urls = []
        for url in post_test_links:
            list_of_urls.append(self.ehen.scrap_for_images(url, 3, 3, 3))
        
        for i in range(len(list_of_urls)):
            self.assertEqual(list_of_urls[i][0], expected_output[i][0])
            #self.assertEqual(list_of_urls[i][1], expected_output[i][1])
            self.assertEqual(list_of_urls[i][2], expected_output[i][2])
            
    def test_scrap_for_images_none(self):
        """
        Tests if scrap_for_images receives None as url, it must return None.
        """
        
        url = None
        response = self.ehen.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
    def test_scrap_for_images_invalid_url(self):
        """
        Tests if scrap_for_images receives an invalid url, it must return None.
        """
        
        url = "None"
        response = self.ehen.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
    def test_gen_gal_name(self):
        """
        Tests the generation of gallery names from urls
        """
        test_url = "https://e-hentai.org/g/1084306/a07bf1a5af/"
        expected = "e-hentai - 1084306 - [nonsummerjack (non)] CANNON SPIKE!"
        
        self.assertEqual(self.ehen.gen_gal_name(test_url,3,3,3), expected)
        
    def test_gen_gal_name_with_cookie(self):
        """
        Tests the generation of gallery names from urls
        """
        test_url = "https://e-hentai.org/g/1310706/2f687a6f59/"
        expected = "e-hentai - 1310706 - Artist Galleries ::: Shiory"
        
        self.assertEqual(self.ehen.gen_gal_name(test_url,3,3,3), expected)
        
    def test_start(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://e-hentai.org/g/1084306/a07bf1a5af/"
        pages = 1
        wait = 2
        retry = 2
        wait_retry = 2
        output = "./"
        
        self.ehen.start(url, pages, None, wait, retry, wait_retry, output)
        
    def test_start_page_2(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://e-hentai.org/g/1084652/bbf0db7388/"
        pages = 2
        wait = 2
        retry = 2
        wait_retry = 2
        output = "./"
        
        self.ehen.start(url, pages, 1, wait, retry, wait_retry, output)
    
    def test_start_clean_needed_page_3_and_4(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://e-hentai.org/g/1087428/b240f1a9ab/"
        pages = 4
        wait = 2
        retry = 2
        wait_retry = 2
        output = "./"
        
        self.ehen.start(url, pages, 2, wait, retry, wait_retry, output)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()