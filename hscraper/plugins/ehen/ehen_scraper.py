import plugin_base


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
        pass
    
    def scrap_for_pages(self):
        """
        Abstract method that scraps html code for pages
        """
        pass
    
    def scrap_for_posts(self):
        """
        Abstract method that scraps html code for posts
        """
        pass
    
    def scrap_for_images(self):
        """
        Abstract method that scraps html code for images
        """
        pass