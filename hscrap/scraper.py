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
        #These a tags contain a relative url, so the domain must be appended too
        links = ["http://danbooru.donmai.us"+a.get("href") for a in tags]
        return links
    
    def scrap_r34(self,html_text):
        """Receives the r34 search result as html text. Returns a list of every image posts url."""
        
        #Seek for post div. Then look for every a tag inside it. Add every url to a list.
        soup = BeautifulSoup(html_text,"html.parser")
        div = soup.find("div",class_="content")
        tags = div.find_all("a")
        #Also uses relative urls
        links = ["https://rule34.xxx/"+a.get("href") for a in tags]
        return links
        
    def scrap_hitomi_la(self,html_text):
        """Receives the hitomi.la hallery as html text. Returns a list of every image posts url."""

        soup = BeautifulSoup(html_text,"html.parser")
        #Look for div which ckass is cover, retrieve its a tag which has the url for the reader
        url_div = soup.find("div",class_="cover")
        url_a = url_div.find("a").get("href")
        #Seek for post ul. Then look for every li tag inside it. We count the the li tags, and generate the urls from there.
        div = soup.find("ul",class_="thumbnail-list")
        tags = div.find_all("li")
        links = ["https://hitomi.la"+url_a+"#"+str(index+1) for index in range(len(tags))]
        return links
        
        
        