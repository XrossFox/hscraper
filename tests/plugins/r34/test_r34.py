import unittest
import sys
sys.path.append('../../../hscraper')

from plugins.r34 import r34_scraper
import re

class Test(unittest.TestCase):


    def setUp(self):
        self.r34 = r34_scraper.R34Scraper()


    def test_scrap_for_pages(self):
        """
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+"
        
        expected_ouput = ["https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=0",
                          "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=42",
                          "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=84",
                          "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=126"]
        
        out = self.r34.scrap_for_pages(given_url, 4)
        for i in range(4):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_scrap_for_pages_skips_from_2(self):
        """
        Tests if skips pages 1 and 2 from 1 to 4
        """
        given_url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+"
        
        expected_ouput = ["https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=84",
                          "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=126"]
        
        out = self.r34.scrap_for_pages(given_url, 4, skip_from=2)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_scrap_for_pages_skip_from_2_to_3(self):
        """
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+"
        
        expected_ouput = ["https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=42",
                          "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=84"]
            
        out = self.r34.scrap_for_pages(given_url, 3, skip_from=1)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_validate_url(self):
        """
        Tests if it validates urls using a regular expression
        """
        
        given_urls = ["https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=42",
                    "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+",
                    "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_a2+-futanari+&pid=0",
                    "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_a2+-futanari+",
                    "https://rule34.xxx/index.php?page=post&s=list&tags=houtengeki"
                          ]
        bad_url = "wrong!"
        
        for url in given_urls:
            self.assertTrue(self.r34.validate_url(url))
        
        self.assertFalse(self.r34.validate_url(bad_url))
        
    def test_validate_url_substring(self):
        """
        Tests that there is only an url present, and not in a form of a substring.
        """
        
        given_url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+&pid=42 a substring"
        
        self.assertFalse(self.r34.validate_url(given_url))
        
    def test_scrap_for_posts(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+"
        
        response = self.r34.scrap_for_posts(url, 1, 1, 1)
        
        pat = re.compile(r'https:\/\/rule34\.xxx\/index\.php\?page=post&s=view&id=[\d]+')
        for post in response:
            self.assertTrue(pat.match(post))

    def test_scrap_for_posts_none(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = None
        
        response = self.r34.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_posts_timed_out_or_not_found(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = "invalid_url"
        
        response = self.r34.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_images(self):
        """
        Tests scrap_for_images for the links it returns
        """
        
        post_test_links = [
            "https://rule34.xxx/index.php?page=post&s=view&id=2964431",
            "https://rule34.xxx/index.php?page=post&s=view&id=2962848",
            "https://rule34.xxx/index.php?page=post&s=view&id=2961609",
            "https://rule34.xxx/index.php?page=post&s=view&id=2959521",
            "https://rule34.xxx/index.php?page=post&s=view&id=2960484"
            ]
        
        expected_output = [
            ('2964431',"https://us.rule34.xxx//images/2665/c7733de0668a709476a03df8b15bb9447e0dfc31.jpg",'jpg'),
            ('2962848',"https://us.rule34.xxx//images/2664/0b0e8004b0b844c7039bb6a7774e8e13.webm","webm"),
            ('2961609',"https://us.rule34.xxx//images/2663/738e50e097633500420816d24ac8bfbf.jpeg",'jpeg'),
            ('2959521',"https://us.rule34.xxx//images/2381/692672a41b219e890b5e6937983e6d67.jpeg",'jpeg'),
            ('2960484',"https://us.rule34.xxx//images/2662/5fe75e8a1c3a39821d7ba9ce63897a02.png?2960484",'png'),
            ]
        
        list_of_urls = []
        for url in post_test_links:
            list_of_urls.append(self.r34.scrap_for_images(url, 3, 3, 3))
        
        for i in range(len(list_of_urls)):
            self.assertEqual(list_of_urls[i][0], expected_output[i][0])
            self.assertEqual(list_of_urls[i][1], expected_output[i][1])
            self.assertEqual(list_of_urls[i][2], expected_output[i][2])
            
    def test_scrap_for_images_deleted_img(self):
        """
        Tests if scrap_for_images can handle deleted images. Must return None in 3 expected indexes.
        """
        
        post_url = "https://rule34.xxx/index.php?page=post&s=view&id=2985053"
        
        res = self.r34.scrap_for_images(post_url, 1, 1, 1)
        
        self.assertFalse(res)
            
            

    def test_scrap_for_images_none(self):
        """
        Tests if scrap_for_images receives None as url, it must return None.
        """
        
        url = None
        response = self.r34.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
    def test_scrap_for_images_invalid_url(self):
        """
        Tests if scrap_for_images receives an invalid url, it must return None.
        """
        
        url = "None"
        response = self.r34.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
    def test_gen_gal_name(self):
        """
        Tests the generation of gallery names from urls
        """
        test_url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_a2+-futanari+"
        expected = "R34_yorha_a2_no-futanari_"
        self.assertEqual(self.r34.gen_gal_name(test_url), expected)
        
    def test_start(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=yorha_2b+-3d+-futanari+-source_filmmaker+"
        pages = 1
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.r34.start(url, pages, None, wait, retry, wait_retry, output)
    
    def test_start_page_2(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=samus_aran+-3d+-source_filmmaker++-futanari+"
        pages = 2
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.r34.start(url, pages, 1, wait, retry, wait_retry, output)
        
    def test_start_page_3_and_4(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://rule34.xxx/index.php?page=post&s=list&tags=-futanari+-3d+mercy+"
        pages = 4
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.r34.start(url, pages, 2, wait, retry, wait_retry, output)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()