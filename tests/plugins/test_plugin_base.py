import sys
import os
sys.path.append('../../hscraper')

import unittest
from bs4 import BeautifulSoup
from plugins import plugin_base

class TestClass(plugin_base.PluginBase):
    
    def start(self):
        pass
    
    def validate_url(self, url):
        pass
    
    def scrap_for_images(self):
        pass
    
    def scrap_for_pages(self):
        pass
    
    def scrap_for_posts(self):
        pass
    
    def gen_gal_name(self, url):
        pass

class Test(unittest.TestCase):
    """
    Test Class for plugin base. It tests the methods that do not need to be overriden across plugins.
    """
    def setUp(self):
        self.pb = TestClass()

    def test_get_html(self):
        """
        Tests the request for an html page
        """
        
        response = self.pb.get_request("https://www.webscraper.io/test-sites/tables",1 ,3, 1)
        parser = BeautifulSoup(response["payload"], "html.parser")
        
        tag = parser.find("h1")
        text = "Table playground"
        
        
        self.assertEqual(tag.text, text)
        self.assertEqual(response["retry"], 1)
        self.assertEqual(response["response_code"], 200)
    
      
    def test_get_html_bad_url(self):
        """
        Tests the request for an html page, given a bad url.
        """
        
        response = self.pb.get_request("https://www.websc/es/taasdasd",1 ,1 ,1)        
        
        self.assertEqual(response["payload"], None)
        self.assertEqual(response["retry"], 1)
        self.assertEqual(response["response_code"], 404)
        
    def test_get_html_bad_url_retry(self):
        """
        Tests the request for an html page, given a bad url, must retry 3 times.
        """
        
        response = self.pb.get_request("https://www.websc/es/taasdasd", 1, 3, 1)
        
        self.assertEqual(response["retry"], 3)
        self.assertEqual(response["response_code"], 404)
        self.assertEqual(response["payload"], None)
        
    def test_create_dir(self):
        """
        Tests the creation of a directory given a path
        """
        
        self.pb.create_dir(path=".", name="test_directory")
        
        self.assertTrue(os.path.exists("test_directory"))
        
        self.pb.create_dir("test_directory","another_test")
        
        self.assertTrue(os.path.exists("test_directory/another_test"))
        
    def test_create_dir_2(self):
        """
        Tests the creation of a directory given a full path
        """
        
        self.pb.create_dir(path="c:\\test", name="test_directory")
        
        self.assertTrue(os.path.exists("c:\\test\\test_directory"))
    
    def test_create_dir_3(self):
        """
        Tests the creation of a directory. Its expected that all white spaces are replaced by '_'
        """
        self.pb.create_dir(path="c:\\test", name="test directory 3 ")
        
        self.assertTrue(os.path.exists("c:\\test\\test_directory_3_"))
    
    def test_create_dir_4(self):
        """
        Tests the creation of a directory for the followin name: [Pixiv] Laserflip / Rosaline (14095911).
        It is expected that it removes invalid chars like slashes
        """
        
        self.pb.create_dir(path="c:\\test", name="[Pixiv] Laserflip / Rosaline (14095911)")
        self.assertTrue(os.path.exists("c:\\test\\[Pixiv]_Laserflip__Rosaline_(14095911)"))
        
    def test_create_invalid_char_dir(self):
        """
        Tests the creation of a directory given an path with invalid characters
        """
        
        self.pb.create_dir(path="?.:", name="test_directory2")
        
        self.assertTrue(os.path.exists("test_directory2"))
        
    def test_write_to_image(self):
        resp = self.pb.get_request("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Facebook_New_Logo_%282015%29.svg/1200px-Facebook_New_Logo_%282015%29.svg.png",
                            wait=1, retry=1, wait_retry=1)
        
        self.pb.write_to(path="", name="le_test.png", payload=bytes(resp['payload']))
        
    def test_gen_string_header(self):
        """
        start() method should call thos at the beginning to print the info of the current task.
        """
        
        url = "test_url"
        pages = 5
        skip_from = 3
        wait = 3
        retry = 3
        wait_retry = 3
        output = "test_ouput_path"
        
        string = self.pb.gen_string_header(url, pages, skip_from, wait, retry, wait_retry, output)
        
        expected_string = ("="*70+"\n\n{0:20}:{1}\n{2:20}:{3}\n{4:20}:{5}\n{6:20}:{7}\n{8:20}:{9}\n{10:20}:{11}\n{12:20}:{13}\n".format(
            "Url",url[:50],"Pages",pages,"From Page",skip_from,"Wait Time",wait,
            "Retries",retry,"Wait Between Retries",wait_retry,"Ouput directorty",output
            ))
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_string_header_no_skip_from(self):
        """
        start() method should call thos at the beginning to print the info of the current task. Test when
        no skip_from param has been passed.
        """
        
        url = "test_url"
        pages = 5
        skip_from = None
        wait = 3
        retry = 3
        wait_retry = 3
        output = "test_ouput_path"
        
        string = self.pb.gen_string_header(url, pages, skip_from, wait, retry, wait_retry, output)
        
        expected_string = ("="*70+"\n\n{0:20}:{1}\n{2:20}:{3}\n{4:20}:{5}\n{6:20}:{7}\n{8:20}:{9}\n{10:20}:{11}\n{12:20}:{13}\n".format(
            "Url",url[:50],"Pages",pages,"From Page","1","Wait Time",wait,
            "Retries",retry,"Wait Between Retries",wait_retry,"Ouput directorty",output
            ))
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_invalid_url_string(self):
        """
        start() method calls this when no valid url is passed. 
        """
        url = "Test_URL.com"
        
        string = self.pb.gen_invalid_url_string(url)
        
        expected_string = ("\n"+">"*4+"Invalid Url in: {}".format(url)+"\n")
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_valid_url_string(self):
        """
        start() method calls this when a valid url is passed. 
        """
        url = "Test_URL.com"
        
        string = self.pb.gen_valid_url_string(url)
        
        expected_string = ("Valid Url in: {}".format(url))
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_scraping_page_string(self):
        """
        start() method calls this when scraping a given page. 
        """
        url = "Test_URL.com"
        
        string = self.pb.gen_scraping_page_string(url)
        
        expected_string = ("\n"+"+"*70+"\nCurrent page: {}\n".format(url)+"-"*70+"\n")
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_downloading_string(self):
        """
        start() method calls this when downloading an image. 
        """
        path = "c:/test/path"
        name = "name.jpg"
        
        string = self.pb.gen_downloading_string(path,name)
        
        expected_string = ("Downloading: {}/{}".format(path,name))
        
        self.assertEqual(string, expected_string)
        
        print(string)
        
    def test_gen_foot_string(self):
        """
        start() method calls this when finished to show output info. 
        """
        downloaded = 65
        pages = 4
        skipped = 1
        failed = 10
        list_failed = ["fail {}".format(n) for n in range(10)]
        
        l_s = ""
        for s in list_failed:
            l_s += s+"\n"
        
        string = self.pb.gen_foot_string(downloaded, pages, skipped, failed, list_failed)
        
        expected_string = ("="*70+"\n{0:20}:{1}\n{2:20}:{3}\n{4:20}:{5}\n{6:20}:{7}\n{8:20}\n{9}".format(
            "Downloaded",downloaded,"Pages",pages,"Skipped",skipped,"Failed",failed,":",l_s)+"="*70)
        
        self.assertEqual(string, expected_string)
        print(string)
        
    def test_gen_page_not_found_string(self):
        """
        start() method calls this when a page is not found
        """
        page_url = "test_url"
    
        string = self.pb.gen_page_not_found_string(page_url)
    
        expected_string = "Couldnt find page: test_url"
    
        self.assertEqual(string, expected_string)
        
    def test_gen_img_not_found_string(self):
        """
        start() method calls this when an image is not found
        """
        img_url = "test_url"
    
        string = self.pb.gen_img_not_found_string(img_url)
    
        expected_string = "Couldnt find image: test_url"
    
        self.assertEqual(string, expected_string)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()