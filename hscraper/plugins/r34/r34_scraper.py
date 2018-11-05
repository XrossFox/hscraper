import plugin_base
import re
from bs4 import BeautifulSoup

class R34Scraper(plugin_base.PluginBase):
    '''
    Class for Danbooru Scraper. Inherits from PluginBase.
    '''
    
    def start(self, url, pages, skip_from, skip_to, wait, retry, wait_retry, output):
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
        
        html_pages = self.scrap_for_pages(url, pages, skip_from, skip_to)
        
        for page in html_pages:
            
            print("Scraping page: {}".format(page))
            posts = self.scrap_for_posts(page, wait, retry, wait_retry)
            
            if posts == None:
                page_not_found.append(page)
                continue
            
            for post in posts:
                
                image = self.scrap_for_images(post, wait, retry, wait_retry)

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
        if len(name) > 100:
            name = name[:100]
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
    
        