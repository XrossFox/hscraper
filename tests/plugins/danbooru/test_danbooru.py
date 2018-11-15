import sys
sys.path.append('../../../hscraper')

from plugins.danbooru import  danbooru_scraper
import unittest
import re


class Test(unittest.TestCase):


    def setUp(self):
        self.dan = danbooru_scraper.Danbooru()

    def test_clean_url_1(self):
        """
        Tests if clean_url removes weid danbooru extras
        From: https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=touhou&ms=1
        To:   https://danbooru.donmai.us/posts?tags=touhou
        """
        weird_url = "https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=touhou&ms=1"
        normal_url = "https://danbooru.donmai.us/posts?tags=touhou"
        
        self.assertEqual(self.dan.clean_url(weird_url), normal_url)
        
    def test_clean_url_2(self):
        """
        Tests if clean_url removes weid danbooru extras
        From: https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=touhou&ms=1
        To:   https://danbooru.donmai.us/posts?tags=touhou
        """
        weird_url = "https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=short_sleeves&ms=1"
        normal_url = "https://danbooru.donmai.us/posts?tags=short_sleeves"
        
        self.assertEqual(self.dan.clean_url(weird_url), normal_url)
        
    def test_scrap_for_pages(self):
        """
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://danbooru.donmai.us/posts?tags=short_sleeves"
        
        expected_ouput = ["https://danbooru.donmai.us/posts?tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=2&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=3&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=4&tags=short_sleeves"]
        
        out = self.dan.scrap_for_pages(given_url, 4)
        for i in range(4):
            self.assertEqual(out[i], expected_ouput[i])
        
            
    def test_scrap_for_pages_skips_from_2(self):
        """
        Tests if skips pages 1 and 2 from 1 to 4
        """
        given_url = "https://danbooru.donmai.us/posts?tags=short_sleeves"
        
        expected_ouput = ["https://danbooru.donmai.us/posts?page=3&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=4&tags=short_sleeves"]
        
        out = self.dan.scrap_for_pages(given_url, 4, skip_from=2)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
            
    def test_scrap_for_pages_skip_from_2_to_3(self):
        """
        It actually doesnt scrap anything, it only generates links for the pages from a given url.
        Tests if links are correctly generated. Must return a list with the urls.
        """
        given_url = "https://danbooru.donmai.us/posts?tags=short_sleeves"
        
        expected_ouput = ["https://danbooru.donmai.us/posts?page=2&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=3&tags=short_sleeves",]
            
        out = self.dan.scrap_for_pages(url=given_url, pages=3, skip_from=1)
        for i in range(2):
            self.assertEqual(out[i], expected_ouput[i])
    
    def test_validate_url(self):
        """
        Tests if it validates urls using a regular expression
        """
        
        given_urls = ["https://danbooru.donmai.us/posts?tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=2&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=3&tags=short_sleeves",
                          "https://danbooru.donmai.us/posts?page=4&tags=touhou+short_sleeves+",
                          ]
        bad_url = "wrong!"
        
        for url in given_urls:
            self.assertTrue(self.dan.validate_url(url))
        
        self.assertFalse(self.dan.validate_url(bad_url))
        
    def test_validate_url_substring(self):
        """
        Tests that there is only an url present, and not in a form of a substring.
        """
        given_url = "https://danbooru.donmai.us/posts?tags=short_sleeves sub"
        
        self.assertFalse(self.dan.validate_url(given_url))
        
    
    def test_scrap_for_posts(self):
        """
        Tests scrap_for_posts returns valid post urls using a regular expression
        """
        
        url = "http://danbooru.donmai.us/posts?tags=touhou"
        
        response = self.dan.scrap_for_posts(url, 1, 1, 1)
        
        pat = re.compile(r'http[s]*:\/\/danbooru\.donmai\.us\/posts\/[\d]+')
        for post in response:
            self.assertTrue(pat.match(post))
            
    def test_scrap_for_posts_none(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = None
        
        response = self.dan.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
        
    def test_scrap_for_posts_timed_out_or_not_found(self):
        """
        Tests scrap_for_posts returns None if sent None as url
        """
        
        url = "invalid_url"
        
        response = self.dan.scrap_for_posts(url, 1, 1, 1)
        
        self.assertTrue(response == None)
            
    def test_scrap_for_images(self):
        """
        Tests scrap_for_images for the links it returns
        """
        
        post_test_links = [
            "https://danbooru.donmai.us/posts/3300197",
            "https://danbooru.donmai.us/posts/3302853",
            "https://danbooru.donmai.us/posts/3302657",
            "https://danbooru.donmai.us/posts/3302649",
            "https://danbooru.donmai.us/posts/3302516",
            "https://danbooru.donmai.us/posts/3240634",
            "https://danbooru.donmai.us/posts/3036340"
            ]
        
        expected_output = [
            ('3300197',"https://danbooru.donmai.us/data/__yorha_no_2_type_b_and_yorha_no_9_type_s_nier_series_drawn_by_von_lemon_vvv__9268fe3ac1215878d2810070c66f97cf.png",'png'),
            ('3302853',"https://danbooru.donmai.us/data/__uraraka_ochako_boku_no_hero_academia_drawn_by_routing_zhengyi__08791b21a033da7222633b2139828ce1.jpg","jpg"),
            ('3302657',"https://danbooru.donmai.us/data/__drawn_by_routing_zhengyi__2c4724cb45e546a66006b9a7cbb8b2ea.jpg",'jpg'),
            ('3302649',"https://danbooru.donmai.us/data/__fire_keeper_dark_souls_and_souls_from_software_drawn_by_routing_zhengyi__8f71e61f810b2bf3e64b9bda90bf4cd2.jpg",'jpg'),
            ('3302516',"https://danbooru.donmai.us/data/__yorha_no_2_type_b_nier_series_and_nier_automata_drawn_by_routing_zhengyi__30f3948719878670106a6757831085c9.jpg",'jpg'),
            ('3240634',"https://danbooru.donmai.us/data/__asui_tsuyu_boku_no_hero_academia_drawn_by_routing_zhengyi__ee1e9db83fe99055f5b0509733d7f7b6.jpg",'jpg'),
            ('3036340',"https://danbooru.donmai.us/data/__albedo_overlord_maruyama_drawn_by_routing_zhengyi__4ad00a94237dd375575cd129a8871fde.jpg",'jpg')
            ]
        
        list_of_urls = []
        for url in post_test_links:
            list_of_urls.append(self.dan.scrap_for_images(url, 3, 3, 3))
        
        for i in range(len(list_of_urls)):
            self.assertEqual(list_of_urls[i][0], expected_output[i][0])
            #self.assertEqual(list_of_urls[i][1], expected_output[i][1])
            self.assertEqual(list_of_urls[i][2], expected_output[i][2])
        
    def test_scrap_for_images_none(self):
        """
        Tests if scrap_for_images receives None as url, it must return None.
        """
        
        url = None
        response = self.dan.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
    def test_scrap_for_images_invalid_url(self):
        """
        Tests if scrap_for_images receives an invalid url, it must return None.
        """
        
        url = "None"
        response = self.dan.scrap_for_images(url, 3, 3, 3)
        
        self.assertEqual(response, None)
        
            
    def test_gen_gal_name(self):
        """
        Tests the generation of gallery names from urls
        """
        test_url = "https://danbooru.donmai.us/posts?tags=routing-zhengyi+1girl+"
        expected = "Danbooru_routing-zhengyi_1girl_"
        
        self.assertEqual(self.dan.gen_gal_name(test_url), expected)

    def test_start_clean_needed(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=han_juri&ms=1"
        pages = 1
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.dan.start(url, pages, None, wait, retry, wait_retry, output)
    
    def test_start_clean_needed_page_2(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=cammy_white+&ms=1"
        pages = 2
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.dan.start(url, pages, 1, wait, retry, wait_retry, output)
        
    def test_start_clean_needed_page_3_and_4(self):
        """
        Tests the whole process, given a valid url
        """
        
        url = "https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=hikari_%28xenoblade_2%29+&ms=1"
        pages = 4
        wait = 3
        retry = 3
        wait_retry = 3
        output = "./"
        
        self.dan.start(url, pages, 2, wait, retry, wait_retry, output)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()