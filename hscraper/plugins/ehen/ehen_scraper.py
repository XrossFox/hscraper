import plugin_base
import re
from bs4 import BeautifulSoup


class EhenScraper(plugin_base.PluginBase):
    '''
    Class for Ehentai Scraper. Inherits from PluginBase.
    '''

    def start(self, url, pages, skip_from, skip_to, wait, retry, wait_retry, output):
        """
        Abstract method for control flow
        """
        pass
    
    def gen_gal_name(self,url):
        pass
    
    def validate_url(self,url):
        """
        Validates URL using a regular expression.
        """
        if re.match(r"https:\/\/e-hentai\.org\/g\/[\d]+\/[\S]{10}[\/\?p=\d+]+", url):
            return True;
        return False
    
    def scrap_for_pages(self, url, pages, skip_from=None, skip_to=None):
        """
        Returns a list of urls for each page given an ehentai url.
        Doesn't really scrap anything. You can set a range to skip certain pages (exclusive in both ends).
        If skip_from is set, it will skip pages until the end, or up to skip_to.
        To use skip_to, skip_from must be set first.
        """
        #request data for retrieval
        url_lists = list()
        
        if not skip_to:
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
        
        response = self.get_request(url, wait, retry, wait_retry)
        
        if response['response_code'] != 200:
            return None

        soup = BeautifulSoup(response['payload'],"html.parser")
        div = soup.find(id="gdt")
        tags = div.find_all("a")
        links = [a.get("href") for a in tags]
        return links
    
    def scrap_for_images(self):
        """
        Abstract method that scraps html code for images
        """
        pass