from plugins import plugin_base
import re
from bs4 import BeautifulSoup


class EhenScraper(plugin_base.PluginBase):
    '''
    Class for Ehentai Scraper. Inherits from PluginBase.
    '''

    def start(self, url, pages, skip_from, wait, retry, wait_retry, output):
        """
        Starts the scraping, and dowloading process
        """
        
        page_not_found = []
        image_not_found = []
        downloaded = 0
        
        print(self.gen_string_header(url, pages, skip_from, wait, retry, wait_retry, output))
        
        if not self.validate_url(url):
            print(self.gen_invalid_url_string(url))
            raise Exception("Not a valid URL")
        else:
            print(self.gen_valid_url_string(url))
        
        f_out = self.create_dir(output, self.gen_gal_name(url, wait, retry, wait_retry))
        
        html_pages = self.scrap_for_pages(url, pages, skip_from)
        
        for page in html_pages:
            
            print(self.gen_scraping_page_string(page))
            posts = self.scrap_for_posts(page, wait, retry, wait_retry)
            
            if posts == None:
                print(self.gen_page_not_found_string(posts))
                page_not_found.append(page)
                continue
            
            for post in posts:
                
                image = self.scrap_for_images(post, wait, retry, wait_retry)

                if image == None:
                    print(self.gen_img_not_found_string(image[1]))
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
             
        print(self.gen_foot_string(downloaded, pages, skip_from, failed, list_failed))
    
    def gen_gal_name(self, url, wait, retry, wait_retry):
        """
        Creates a name for the gallery from the title of the gallery.
        """
        req = self.get_request(url, wait, retry, wait_retry, cookies=dict(nw="1"))
        
        h = BeautifulSoup(req['payload'], "html.parser")
        
        name = h.find(id="gn").contents
        
        tags = url.split("/")
        name = "e-hentai - "+ str(tags[-3]) + " - " +name[0]
        return name
    
    def validate_url(self,url):
        """
        Validates URL using a regular expression.
        """
        return re.match(r"^https:\/\/e-hentai\.org\/g\/[\d]+\/[\S]{10}[\/\?p=\d+]+$", url)
    
    def scrap_for_pages(self, url, pages, skip_from=None):
        """
        Returns a list of urls for each page given an ehentai url.
        Doesn't really scrap anything. You can set a range to skip certain pages (exclusive in both ends).
        If skip_from is set, it will skip pages until the end, or up to skip_to.
        To use skip_to, skip_from must be set first.
        """
        #request data for retrieval
        url_lists = list()
        
        skip_to = pages
            
        if not skip_from:
            skip_from = 0
        
        for page in range(skip_from + 1, skip_to+1):
            if page > 1:
                url_lists.append(url+'?p='+str(page-1))
            else:
                url_lists.append(url)
        return url_lists
    
    def scrap_for_posts(self, url, wait, retry, wait_retry):
        """
        Scraps all post url in a given page. Returns a list of links to each post.
        If it receives an invalid url or None, it returns None.
        """
        if url == None:
            return None
        
        response = self.get_request(url, wait, retry, wait_retry, cookies=dict(nw="1"))
        
        if response['response_code'] != 200:
            return None

        soup = BeautifulSoup(response['payload'],"html.parser")
        div = soup.find(id="gdt")
        tags = div.find_all("a")
        links = [a.get("href") for a in tags]
        return links
    
    def scrap_for_images(self, url, wait, retry, wait_retry):
        """
        Receives the URL to a post, returns the number of the post, the URL and file extensions
        to the image as a tuple. If it receives an invalid url or None, it returns None.
        """
        
        if url == None:
            return None
        
        html = self.get_request(url, wait, retry, wait_retry)
        
        if html["response_code"] != 200:
            return None
        
        soup = BeautifulSoup(html['payload'], "html.parser")

        img_tag = soup.find(id="img")
        img_url = img_tag.get("src")
        
        name = url.split("/")
        extension = img_url.split(".")
        return (str(name[-1]), img_url, extension[-1])