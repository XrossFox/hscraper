from plugins import plugin_base
import re
from bs4 import BeautifulSoup


class HitomiScraper(plugin_base.PluginBase):
    '''
    Class for hitomi.la Scraper. Inherits from PluginBase.
    '''
    # Note, this scraper works a bit different from the other 3. Most notably in the scrap methods
    
    def gen_gal_name(self, url):
        """
        Creates a name for the gallery as follows: hitomi_la_numberOfGallery
        """
        url_parts = url.split("/")
        name = "hitomi_la_"+ url_parts[-1].split(".")[0]
        return name

    def scrap_for_images(self, url):
        """
        Mangles the urls to get its name, url and file extension
        """

        url_parts = url.split("/")
        name = url_parts[-1].split(".")[0]
        extension = url_parts[-1].split(".")[-1]
        
        return(name,url,extension)
                
    def scrap_for_pages(self, url):
        """
        Gets the page of the reader (from hitomi.la) given a gallery url.
        """
        if re.match(r"\bhttps:\/\/hitomi\.la\/galleries\/[\d]+\.html\b", url):
            url = url.replace("galleries","reader")
            url +="#1"
            
        elif re.match(r"\bhttps:\/\/hitomi\.la\/reader\/[\d]+\.html#[\d]+\b", url):
            return url
        
        return url
    
    def scrap_for_posts(self, url, wait, retry, wait_retry, from_img=None, to_img=None):
        """
        Scraps all post url in a given page. Returns a list of links to each image in the reader.
        If it receives an invalid url or None, it returns None. You can set a range
        to skip certain images (exclusive left, inclusive right). If from_img is set, it will skip pages until
        the end, or up to to_img. If to_img is not set, returns all pages.
        """
        if url == None:
            return None
        
        response = self.get_request(url, wait, retry, wait_retry)
        
        if response['response_code'] != 200:
            return None
        
        soup = BeautifulSoup(response['payload'], "html.parser")
        
        divs = soup.find_all("div",class_="img-url")
        texts = [div.text for div in divs]
        
        urls = []
        
        for text in texts:
            tmp = text.split("/")
            if int(tmp[-2][-1]) in [0,1]:
                text = text.replace("//g.","https://aa.")
            elif (int(tmp[-2][-1]) % 2) > 0 :
                text = text.replace("//g.","https://ba.")
            else: text = text.replace("//g.","https://aa.")
            urls.append(text)
        
        if from_img and to_img:
            return urls[from_img:to_img]
        elif to_img:
            return urls[:to_img]
        
        return urls
    
    
    
    def start(self, url, from_img, to_img, wait, retry, wait_retry, output):
        """
        Starts the scraping, and dowloading process
        """
        
        print(self.gen_string_header(url, to_img, from_img, wait, retry, wait_retry, output))
        
        page_not_found = []
        image_not_found = []
        downloaded = 0
        
        if not self.validate_url(url):
            print(self.gen_invalid_url_string(url))
            raise Exception("Not a valid URL")
        else:
            print(self.gen_valid_url_string(url))
        
        f_out = self.create_dir(output, self.gen_gal_name(url))
        
        html_pages = self.scrap_for_pages(url)
        
        for page in [html_pages]:
            
            print(self.gen_scraping_page_string(page))
            posts = self.scrap_for_posts(page, wait, retry, wait_retry, from_img, to_img)

            
            for post in posts:
                
                #print(self.gen_page_not_found_string(posts))
                image = self.scrap_for_images(post)

                if image == None:
                    print(self.gen_img_not_found_string(post))
                    image_not_found.append(post)
                    continue
                
                img_data = self.get_request(image[1], wait, retry, wait_retry)
                
                try:
                    print(self.gen_downloading_string(f_out, image[0]+"."+image[2]))
                    self.write_to(f_out, "{}.{}".format(image[0],image[2]), img_data['payload'])
                    downloaded += 1
                except:
                    print(self.gen_img_not_found_string(image[1]))
                    image_not_found.append(post)
                    continue
                
        failed = len(page_not_found) + len(image_not_found)
        list_failed = []
        list_failed.extend(page_not_found)
        list_failed.extend(image_not_found)
             
        print(self.gen_foot_string(downloaded, to_img, from_img, failed, list_failed))
     
    
    def validate_url(self, url):
        """
        Validates the url from either, the gallery or the reader
        """
        return re.match(r"^https:\/\/hitomi\.la\/reader\/[\d]+\.html#[\d]+$", url) or re.match(r"^https:\/\/hitomi\.la\/galleries\/[\d]+\.html$", url)
        