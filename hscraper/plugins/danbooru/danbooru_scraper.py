import plugin_base

class Danbooru(plugin_base.PluginBase):
    '''
    Class for Danbooru Scraper. Inherits from PluginBase.
    '''
    
    def start(self, url, pages, skip_pages, wait, retries, wait_retries, output):
        pass
    
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
        #https://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=touhou&ms=1
        #https://danbooru.donmai.us/posts?tags=touhou
        pass
    
    def scrap_for_images(self):
        pass
    
    def scrap_for_posts(self):
        pass
    
    def scrap_for_pages(self, url, pages, skip_from=None, skip_to=None):
        """
        Returns a list of urls for each page. Doesn really scraps anything. You can set a range
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
        