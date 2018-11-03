import plugin_base
import re
from bs4 import BeautifulSoup

class R34Scraper(plugin_base.PluginBase):
    '''
    Class for Danbooru Scraper. Inherits from PluginBase.
    '''
    
    def start(self, url, pages, skip_from, skip_to, wait, retry, wait_retry, output):
        pass
    
    def validate_url(self, url):
        """
        Validates URL using a regular expression.
        """
        if re.match(r"https:\/\/rule34\.xxx\/index\.php\?page=post&s=list&tags=[\S]+\+(&pid=[\d]+)*", url):
            return True;
        return False
    
    def gen_gal_name(self, url):
        """
        Creates a name for the gallery as follows: Danbooru_tag1_tag2_tagN_
        """
        tags = url.split("=")
        name = "R34_"+ tags[-1].replace("+","_").replace("-","no-")
        return name
    
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
        
        img_tag_original = soup.find("a",{"onclick":"Post.highres(); $('resized_notice').hide(); Note.sample=false; return false;",
                                "style":"font-weight: bold;"})
        img_tag_normal = soup.find(id="image")
        video_tag = soup.find(name="video",id="gelcomVideoPlayer")
        
        
        if img_tag_original:
            img_url = img_tag_original.get("href")
        elif img_tag_normal:
            img_url = img_tag_normal.get("src")
        else:
            img_url = video_tag.find("source").get("src")    
        
        name = url.split("=")
        
        extension = img_url.split(".")
        extension = extension[-1]
        
        if re.match(r"[\S]+\?[\d]+", extension):
            extension = extension.split("?")
            extension = extension[0]
        
        return (str(name[-1]), img_url, extension)
    
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
        div = soup.find("div",class_="content").find("div")
        tags = div.find_all("a")

        links = ["https://rule34.xxx/"+a.get("href") for a in tags]
        return links
    
    def scrap_for_pages(self, url, pages, skip_from=None, skip_to=None):
        """
        Returns a list of urls for each page. Doesn't really scrap anything. You can set a range
        to skip certain pages (exclusive in both ends). If skip_from is set, it will skip pages until
        the end, or up to skip_to. To use skip_to, skip_from must be set first.
        """

        url_lists = list()
        
        if not skip_to:
            skip_to = pages
            
        if not skip_from:
            skip_from = 0
        
        for page in range(skip_from + 1, skip_to+1):
            if page > 1:
                url_lists.append(url+"&pid="+str(42*(page-1)))
            else:
                url_lists.append(url+"&pid="+str(0))
        return url_lists
    
        