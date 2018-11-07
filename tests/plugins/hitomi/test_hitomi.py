import sys
sys.path.append('../../../hscraper/plugins')
sys.path.append('../../../hscraper/plugins/hitomi')
import hitomi_scraper
import unittest
import re


class Test(unittest.TestCase):
    
    def setUp(self):
        self.hit = hitomi_scraper.HitomiScraper()
        
    def test_validate_url_valid_gallery_1(self):
        """
        Tests if it validates urls using a regular expressions. valid gallery URL.
        """
        
        given_urls = "https://hitomi.la/galleries/1305683.html"
        
        self.assertTrue(self.hit.validate_url(given_urls))
        
    def test_validate_url_valid_gallery_2(self):
        """
        Tests if it validates urls using a regular expressions. valid gallery URL.
        """
        
        given_urls = "https://hitomi.la/galleries/1307822.html"
        
        self.assertTrue(self.hit.validate_url(given_urls))
        
    def test_validate_url_valid_reader_1(self):
        """
        Tests if it validates urls using a regular expressions. valid reader URL.
        """
        
        given_urls = "https://hitomi.la/reader/1305683.html#1"
        
        self.assertTrue(self.hit.validate_url(given_urls))
        
    def test_validate_url_valid_reader_2(self):
        """
        Tests if it validates urls using a regular expressions. valid reader URL.
        """
        
        given_urls = "https://hitomi.la/reader/1307822.html#1"
        
        self.assertTrue(self.hit.validate_url(given_urls))

    def test_scrap_for_pages_1(self):
        """
        Test for gallery url.
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://hitomi.la/galleries/1307822.html"
        
        expected_ouput = ["https://hitomi.la/reader/1307822.html#1"]
        
        out = self.hit.scrap_for_pages(given_url)
        self.assertEqual(out, expected_ouput[0])
        
    def test_scrap_for_pages_2(self):
        """
        Test for reader url.
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://hitomi.la/reader/1305683.html#1"
        
        expected_ouput = ["https://hitomi.la/reader/1305683.html#1"]
        
        out = self.hit.scrap_for_pages(given_url)
        self.assertEqual(out, expected_ouput[0])
        
    def test_scrap_for_posts_1(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression. galleries that end
        in odd number have an url: aa.like.this
        """
        
        url = "https://hitomi.la/reader/1305683.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, 9)
        
        pat = re.compile(r'\bhttps:\/\/ba\.hitomi\.la\/galleries\/[\d]+\/[\S]+\b')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_2(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression. galleries that end in 
        even number have an url: ab.url.like.this
        """
        
        url = "https://hitomi.la/reader/1307822.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, 9)
        
        pat = re.compile(r'\bhttps:\/\/aa\.hitomi\.la\/galleries\/[\d]+\/[\S]+\b')
        for post in response:
            self.assertTrue(pat.match(post))

    def test_scrap_for_posts_3(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression. galleries that end in 1 or 0
        have an url like this aa.rest.of.the.url
        """
        
        url = "https://hitomi.la/reader/1027141.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, 9)
        
        pat = re.compile(r'\bhttps:\/\/aa\.hitomi\.la\/galleries\/[\d]+\/[\S]+\b')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_4(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression. galleries that end in 1 or 0
        have an url like this aa.rest.of.the.url
        """
        
        url = "https://hitomi.la/reader/1311140.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, 9)
        
        pat = re.compile(r'\bhttps:\/\/aa\.hitomi\.la\/galleries\/[\d]+\/[\S]+\b')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_no_pages_specified(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression, with no pages specified
        """
        
        url = "https://hitomi.la/reader/1305683.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1)
        
        pat = re.compile(r'\bhttps:\/\/[ab]*a\.hitomi\.la\/galleries\/[\d]+\/[\S]+\b')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_none_url(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = None
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_posts_invalid_url(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = "im an invalid url"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_posts_pages_to_3(self):
        """
        Tests scrap_for_posts returns valid img urls up to image 3
        """
        
        url = "https://hitomi.la/reader/1305683.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, to_img=3)
        self.assertEqual(response[0],"https://ba.hitomi.la/galleries/1305683/1.png")
        self.assertEqual(response[1],"https://ba.hitomi.la/galleries/1305683/2.png")
        self.assertEqual(response[2],"https://ba.hitomi.la/galleries/1305683/3.png")
        
    def test_scrap_for_posts_pages_from_2_to_4(self):
        """
        Tests scrap_for_posts returns valid post urls from img 2 to 4.
        """
        
        url = "https://hitomi.la/reader/1307822.html#1"
        
        response = self.hit.scrap_for_posts(url, 2, 1, 1, from_img=2, to_img=4)
        self.assertEqual(response[0],"https://aa.hitomi.la/galleries/1307822/003_RJ237179_img_smp2.jpg")
        self.assertEqual(response[1],"https://aa.hitomi.la/galleries/1307822/004_01.jpg")
        
    def test_scrap_for_posts_pages(self):
        """
        Tests scrap_for_images for the links it returns. It only mangles the url for data.
        """
        
        post_test_links = [
            "https://ba.hitomi.la/galleries/1305683/1.png",
            "https://ba.hitomi.la/galleries/1305683/2.png",
            "https://ba.hitomi.la/galleries/1305683/3.png",
            ]
        
        expected_output = [
            ('1',"https://ba.hitomi.la/galleries/1305683/1.png",'png'),
            ('2',"https://ba.hitomi.la/galleries/1305683/2.png","png"),
            ('3',"https://ba.hitomi.la/galleries/1305683/3.png",'png'),
        ]
        
        list_of_urls = []
        for url in post_test_links:
            list_of_urls.append(self.hit.scrap_for_images(url))
        
        for i in range(len(list_of_urls)):
            self.assertEqual(list_of_urls[i][0], expected_output[i][0])
            self.assertEqual(list_of_urls[i][1], expected_output[i][1])
            self.assertEqual(list_of_urls[i][2], expected_output[i][2])

    def test_scrap_for_posts_pages_2(self):
        """
        Tests scrap_for_images for the links it returns. It only mangles the url for data.
        """
        
        post_test_links = [
            "https://aa.hitomi.la/galleries/1307822/003_RJ237179_img_smp2.jpg",
            "https://aa.hitomi.la/galleries/1307822/004_01.jpg",
            ]
        
        expected_output = [
            ('003_RJ237179_img_smp2',"https://aa.hitomi.la/galleries/1307822/003_RJ237179_img_smp2.jpg",'jpg'),
            ('004_01',"https://aa.hitomi.la/galleries/1307822/004_01.jpg","jpg"),
        ]
        
        list_of_urls = []
        for url in post_test_links:
            list_of_urls.append(self.hit.scrap_for_images(url))
        
        for i in range(len(list_of_urls)):
            self.assertEqual(list_of_urls[i][0], expected_output[i][0])
            self.assertEqual(list_of_urls[i][1], expected_output[i][1])
            self.assertEqual(list_of_urls[i][2], expected_output[i][2])
    
    def test_gen_gal_name(self):
        """
        Tests the generation of gallery names from urls
        """
        test_url = "https://hitomi.la/reader/1305683.html#1"
        expected = "hitomi_la_1305683"
        
        self.assertEqual(self.hit.gen_gal_name(test_url), expected)
        
    def test_start_1(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://hitomi.la/galleries/1305683.html"
        from_img = None
        to_img = None
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.hit.start(url, from_img, to_img, wait, retry, wait_retry, output)
        
    def test_start_2(self):
        """
        Tests the whole process, given a valid url, from img 5 to 15
        """
        
        url = "https://hitomi.la/galleries/1307822.html"
        from_img = 4
        to_img = 15
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.hit.start(url, from_img, to_img, wait, retry, wait_retry, output)
        
    def test_start_3(self):
        """
        Tests the whole process, given a valid url, given 0 pages, it must scrap all images.
        """
        
        url = "https://hitomi.la/galleries/1027141.html"
        from_img = 0
        to_img = 0
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.hit.start(url, from_img, to_img, wait, retry, wait_retry, output)
        
    def test_start_4(self):
        """
        Tests the whole process, given a valid url, given 0 pages, it must scrap all images.
        """
        
        url = "https://hitomi.la/galleries/1311140.html"
        from_img = 0
        to_img = 0
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.hit.start(url, from_img, to_img, wait, retry, wait_retry, output)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()