import plugin_base
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
    
    def scrap_for_posts(self, url, wait, retry, wait_retry, from_img=None, to_img=None, ):
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
            if (int(tmp[-2][-1]) % 2) > 0 :
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
        
        page_not_found = []
        image_not_found = []
        
        if not self.validate_url(url):
            raise Exception("Not a valid URL: {}".format(url))
        else:
            print("Valid URL: {}".format(url))
        
        f_out = self.create_dir(output, self.gen_gal_name(url))
        print("Output Directory is: {}".format(f_out))
        
        html_pages = self.scrap_for_pages(url)
        
        for page in [html_pages]:
            
            print("Scraping page: {}".format(page))
            posts = self.scrap_for_posts(page, wait, retry, wait_retry, from_img, to_img)

            
            for post in posts:
                
                image = self.scrap_for_images(post)

                if image == None:
                    image_not_found.append(post)
                    continue
                
                print("Downloading image in: {}".format(image[1]))
                img_data = self.get_request(image[1], wait, retry, wait_retry)
                
                print("Downloading image to: {}/{}.{}".format(f_out,image[0],image[2]))
                self.write_to(f_out, "{}.{}".format(image[0],image[2]), img_data['payload'])
                
        if len(page_not_found) > 0:
            print("Pages not found: {}".format(len(page_not_found)))
            for page in page_not_found:
                print("-"*4+page)
                
        if len(image_not_found) > 0:
            print("Images not found: {}".format(len(image_not_found)))
            for img in image_not_found:
                print("+"*4+img)
     
    
    def validate_url(self, url):
        if re.match(r"\bhttps:\/\/hitomi\.la\/reader\/[\d]+\.html#[\d]+\b", url) or re.match(r"\bhttps:\/\/hitomi\.la\/galleries\/[\d]+\.html\b", url):
            return True
        
        return False