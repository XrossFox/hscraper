'''
Created on 30/03/2018

@author: XrossFox
'''
from bs4 import BeautifulSoup

class Scraper(object):
    '''
    Contains methods for html scraping and a tag retrieval.
    '''
    
    def scrap_ehentai(self,html_text):
        """Receives the ehentai gallery as html text. Returns a list of every image posts url."""
        
        #Seek for gdt div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find(id="gdt")
        tags = div.find_all("a")
        links = [a.get("href") for a in tags]
        return links
    
    def scrap_danbooru(self,html_text):
        """Receives the danbooru search result as html text. Returns a list of every image posts url."""
        
        #Seek for post div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find(id="posts")
        tags = div.find_all("a")
        #These a tag contains a partial url, so the domain must be appended too
        links = ["http://danbooru.donmai.us"+a.get("href") for a in tags]
        return links
        
        
        