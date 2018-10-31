import plugin_base
import re
from bs4 import BeautifulSoup

class Danbooru(plugin_base.PluginBase):
    '''
    Class for Danbooru Scraper. Inherits from PluginBase.
    '''
    
    def start(self, url, pages, skip_from, skip_to, wait, retry, wait_retry, output):
        url = self.clean_url(url)
        
        if not self.validate_url(url):
            raise Exception("Not a valid URL: {}".format(url))
        else:
            print("Valid URL: {}".format(url))
        
        f_out = self.create_dir(output, self.gen_gal_name(url))
        print("Output Directory is: {}".format(f_out))
        
        pages = self.scrap_for_pages(url, pages, skip_from, skip_to)
        
        for page in pages:
            print("Scraping page: {}".format(page))
            posts = self.scrap_for_posts(page, wait, retry, wait_retry)
            
            for post in posts:
                
                image = self.scrap_for_images(post, wait, retry, wait_retry)
                print("Downloading image in: {}".format)
                img_data = self.get_request(image[1], wait, retry, wait_retry)
                print("Downloading image to: {}/{}".format(f_out,image[0]))
                self.write_to(f_out, image[0], img_data)
            
     
    
    def gen_gal_name(self, url):
        """
        Creates a name for the gallery as follows: Danbooru_tag1_tag2_tagN_
        """
        tags = url.split("=")
        name = "Danbooru_"+ tags[-1].replace("+","_")
        return name
        
    def clean_url(self,url):
        """
        Normalizes danbooru weird urls. Returns an url without weird characters.
        """
        #https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=touhou&ms=1
        #https://danbooru.donmai.us/posts?tags=touhou
        url = url.replace("utf8=%E2%9C%93&","")
        url = url.replace("&ms=1","")
        return url
    
    def validate_url(self, url):
        """
        Validates URL using a regular expression.
        """
        if re.match(r"https:\/\/danbooru\.donmai\.us\/posts\?[page=\d+&]*tags=[\w\d+]+", url):
            return True;
        return False
    
    def scrap_for_images(self, url, wait, retry, wait_retry):
        """
        Receives the URL to a post, returns the number of the post and the URL to the image as
        a tuple.
        """
        
        html = self.get_request(url, wait, retry, wait_retry)
        
        soup = BeautifulSoup(html['payload'], "html.parser")
        
        resize = soup.find(id="image-resize-link")
        
        if resize:
            img_url = resize.get("href")
        else:
            img_tag = soup.find(id="image")
            img_url = img_tag.get("src")
        
        name = url.split("/")
        return (str(name[-1]), img_url)
    
    def scrap_for_posts(self, url, wait, retry, wait_retry):
        """
        Scraps all post url in a given page. Returns a list of links to each post.
        """
        
        response = self.get_request(url, wait, retry, wait_retry)
        #Seek for post div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(response['payload'],"html.parser")
        div = soup.find(id="posts-container")
        tags = div.find_all("a")
        #These a tags contain a relative url, so the domain must be appended too
        links = ["https://danbooru.donmai.us"+a.get("href") for a in tags]
        return links
    
    def scrap_for_pages(self, url, pages, skip_from=None, skip_to=None):
        """
        Returns a list of urls for each page. Doesn't really scrap anything. You can set a range
        to skip certain pages (exclusive in both ends). If skip_from is set, it will skip pages until
        the end, or up to skip_to. To use skip_to, skip_from must be set first.
        """
        #https://danbooru.donmai.us/posts?tags=short_sleeves"
        url_lists = list()
        
        if not skip_to:
            skip_to = pages
            
        if not skip_from:
            skip_from = 0
        
        for page in range(skip_from + 1, skip_to+1):
            if page > 1:
                url_lists.append("?page={}&".join(url.split(sep="?")).format(page))
            else:
                url_lists.append(url)
        return url_lists
        