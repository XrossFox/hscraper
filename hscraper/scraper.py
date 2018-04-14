'''
Created on 30/03/2018

@author: XrossFox
'''
from bs4 import BeautifulSoup
from hscraper import web_retriever

class Scraper(object):
    '''
    Contains methods for html scraping and a tag retrieval.
    '''
    #---
    def scrap_ehentai(self,html_text):
        """Receives the ehentai gallery as html text. Returns a touple of (gallery title, a list of every image posts url)."""
        
        #Seek for gdt div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find(id="gdt")
        tags = div.find_all("a")
        links = [a.get("href") for a in tags]
        return (soup.find("title").text,links)
    
    def scrap_danbooru(self,html_text):
        """Receives the danbooru search result as html text. Returns a touple of (gallery title, a list of every image posts url)."""
        
        #Seek for post div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find(id="posts").find("div",style="overflow: hidden;")
        tags = div.find_all("a")
        #These a tags contain a relative url, so the domain must be appended too
        links = ["http://danbooru.donmai.us"+a.get("href") for a in tags]
        return (soup.find("title").text,links)
    
    def scrap_r34(self,html_text):
        """Receives the r34 search result as html text. Returns a touple of (gallery title, a list of every image posts url)."""
        
        #Seek for post div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find("div",class_="content").find("div")
        tags = div.find_all("a")
        #Also uses relative urls
        links = ["https://rule34.xxx/"+a.get("href") for a in tags]
        return (soup.find("title").text,links)
    
    def scrap_hitomi(self,html_text):
        """Returns the name of the page"""
        soup = BeautifulSoup(html_text,"html.parser")
        return (soup.find("title").text)
    #---    
        
    def scrap_post_ehentai(self,post_url,wait=1):
        """Receives an url to an image post from ehentai, and looks for the image in it"""
        #Downloads the html doc
        #Then looks for the img tag with id=img
        #Returns the src attribute of the img tag as a string
        
        web = web_retriever.WebRetriever()
        html = web.retrieve_web_page(post_url, wait)
        
        soup = BeautifulSoup(html, "html.parser")
        img_tag = soup.find(id="img")
        img_url = img_tag.get("src")
        return img_url
    
    def scrap_post_danbooru(self,post_url,wait=1):
        """Receives an url to an image post from danbooru, and looks for the image in it"""
        #Downloads the html doc
        #Then looks for the img tag with id=image
        #Returns the src attribute of the img tag as a string
        
        web = web_retriever.WebRetriever()
        html = web.retrieve_web_page(post_url, wait)
        
        soup = BeautifulSoup(html, "html.parser")
        img_tag = soup.find(id="image")
        img_url = img_tag.get("src")
        
        #More relative urls, matey
        return img_url
    
    def scrap_post_r34(self,post_url,wait=1):
        """Receives an url to an image post from danbooru, and looks for the image in it"""
        #Downloads the html doc
        #Then looks for the img tag with id=image
        #Returns the src attribute of the img tag as a string
        
        web = web_retriever.WebRetriever()
        html = web.retrieve_web_page(post_url, wait)
        
        soup = BeautifulSoup(html, "html.parser")
        try:
            img_tag = soup.find(id="image")
            img_url = img_tag.get("src")
        except:
            img_url = soup.find("video").get("src")

        return img_url

    #---
    
    def scrap_post_hitomi_la(self,html,wait=1):
        """Receives an url to the reader from hitomi.la, and looks for all the image urls in it. 
        Returns a touple of (gallery title, a list of every image url)"""
        
        '''One step is skipped in case of scrapping a gallery from hitomi.la, since the 
        siteworks quite differently. Instead the link to the reader is passes directly
        and then all image links are scrapped from there'''
        
        #Downloads the html doc
        #Then look for every div which class is class=img-url
        #Process the text inside the divs so it resembles a proper url
        #Return al img urls
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all("div",class_="img-url")
        texts = [div.text for div in divs]
        urls = ["https://0a.hitomi.la/galleries/"+text.split(sep="/")[-2]+"/"+text.split(sep="/")[-1] for text in texts]
        return urls
