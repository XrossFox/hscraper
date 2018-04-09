'''
Created on 21/02/2018

@author: David
'''
import os
import errno
from hscrap import web_retriever
from hscrap import scraper
class HCore():
    
    def user_input(self,url,no_pages,output_path = os.path.dirname(__file__)+"\\",wait=1):
        """Receives url, number of pages and optional output path. Starts the process."""
        #Meant for process control, calls every other method that does the work.
        
        #check url
        self._check_url_domain(url)
        #get htmls
        html_list = self._generate_links(url, no_pages, wait)
        #img posts
        img_posts = self._get_img_posts(url,html_list)
        #create output dir and download images
     
    def _get_images(self,url,img_posts=[]):
        """Discriminates between domains to call the apropiate img post scraper"""
        if("https://e-hentai.org/" in url):
            return scraper.Scraper.scrap_
        if("http://danbooru.donmai.us" in url):
            return web_retriever.WebRetriever().retrieve_danbooru(url, no_pages, wait)
        if("https://rule34.xxx/" in url):
            return web_retriever.WebRetriever().retrieve_r34(url, no_pages, wait)
        if("https://hitomi.la/" in url):
            return [-1]
        raise Exception("Not a proper url to generate was received")        
        
    def _generate_links(self,url,no_pages,wait):
        """Discriminates between domains to call the apropiate link generator"""
        if("https://e-hentai.org/" in url):
            return web_retriever.WebRetriever().retrieve_ehentai(url, no_pages, wait)
        if("http://danbooru.donmai.us" in url):
            return web_retriever.WebRetriever().retrieve_danbooru(url, no_pages, wait)
        if("https://rule34.xxx/" in url):
            return web_retriever.WebRetriever().retrieve_r34(url, no_pages, wait)
        if("https://hitomi.la/" in url):
            return [-1]
        raise Exception("Not a proper url to generate was received")
    
    def _get_img_posts(self,url,html_list=[]):
        """Discriminates between domains to call the apropiate scraper"""
        if("https://e-hentai.org/" in url):
            post_urls = []
            for html in html_list:
                post_urls += scraper.Scraper.scrap_ehentai(self, html)
            return post_urls
        if("http://danbooru.donmai.us" in url):
            post_urls = []
            for html in html_list:
                post_urls += scraper.Scraper.scrap_danbooru(self, html)
            return post_urls
        if("https://rule34.xxx/" in url):
            post_urls = []
            for html in html_list:
                post_urls += scraper.Scraper.scrap_r34(self, html)
            return post_urls
        if("https://hitomi.la/" in url):
            return [-1]
        raise Exception("Couldn't get any post from your url")
    
    def _check_url_domain(self,url):
        """Validates a webpage's domain in url for a supported site"""
        supported_domains = ["e-hentai.org","danbooru.donmai.us","rule34.xxx","hitomi.la"]
        
        for domain in supported_domains:
            if url.find(domain) > 0:
                return
        raise Exception("Not a supported website found")
    
    def create_output_dir(self,path,dir_name):
        """Creates a directory according to path and folder name"""
        try:
            #This bullshit right here is to remove character that arent supported in directory names. I got lazy and copy pasted themselves :P
            dir_name = dir_name.replace("|"," ").replace("<"," ").replace(">", " ").replace(":", " ").replace("\"", " ").replace("\\", " ")
            dir_name = dir_name.replace("/"," ").replace("?"," ").replace("*", " ")
            os.makedirs(path+dir_name)
            return path+dir_name
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise