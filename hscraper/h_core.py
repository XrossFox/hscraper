'''
Created on 21/02/2018

@author: David
'''
#This adds the whole root folder to python path
import os
import sys
local = os.path.dirname(os.path.realpath(__file__))
root_path = local.split("\\")
string = ""
for p in range(len(root_path)-1):
    string += root_path[p]+"\\"
print(string)
sys.path.append(string)
from hscraper import web_retriever
from hscraper import scraper
import click
class HCore():
    
    def user_input(self,url,no_pages,output_path,wait=1):
        """Receives url, number of pages and optional output path. Starts the process."""
        #Meant for process control, calls every other method that does the work.
        
        #check url
        print("Validating Url")
        self._check_url_domain(url)
        
        #check pages
        print("Validating Pages")
        self._check_for_pages(no_pages)
        
        #retrieve htmls
        print("Rerieving pages from the internet...")
        html_list = self._generate_links(url, no_pages, wait)
        #scrap the htmls for each post url
        print("Scraping...")
        posts = self._scrap_posts(url,html_list)
        #create output dir and download images. I ended up with a list of touples with a touple and list inside it. Derp
        print("The gallery Name is: "+posts[0].strip())
        gallery_name = posts[0]
        final_destination = self.create_output_dir(output_path, gallery_name)
        
        #scrap posts for each image url
        print("Looking for pictures...")
        imgs_urls = self._scrap_imgs(url,posts,wait)
        #download images!
        print("Downloading " +str(len(imgs_urls))+" picture/s")
        self._download_images(imgs_urls,final_destination,wait)
        
        print("My job here is done!")
        
    def _download_images(self,imgs_urls,final_destination,wait=1):
        """Downloads all images in a list"""
        for url in imgs_urls:
            web_retriever.WebRetriever().retrieve_image(url, final_destination, wait)
        
    def _check_for_pages(self,no_pages):
        try:
            return no_pages in range(1,100)
        except:
            raise Exception("Invalid number of pages. Check that it is a positive integral number.")
    
    
    
    def _scrap_imgs(self,url,posts=[],wait=1):
        """Discriminates between domains to call the apropiate post scraper"""
        img_url_list = []
        if("https://e-hentai.org/" in url):
            #Position 1 is the one with the list of posts urls
            for post in posts[1]:
                img_url_list.append(scraper.Scraper.scrap_post_ehentai(self, post, wait))
            return img_url_list
        if("danbooru.donmai.us" in url):
            for post in posts[1]:
                img_url_list.append(scraper.Scraper.scrap_post_danbooru(self, post, wait))
            return img_url_list
        if("https://rule34.xxx/" in url):
            for post in posts[1]:
                img_url_list.append(scraper.Scraper.scrap_post_r34(self, post, wait))
            return img_url_list
        if("https://hitomi.la/" in url):
            img_url_list = scraper.Scraper.scrap_post_hitomi_la(self, posts[1][0], wait)
            return img_url_list
        raise Exception("Not a proper url to generate was received")
    
           
    def _generate_links(self,url,no_pages,wait):
        '''Discriminates between domains to call the apropiate web retriever to get the html docs'''
        
        if("https://e-hentai.org/" in url):
            return web_retriever.WebRetriever().retrieve_ehentai(url, no_pages, wait)
        if("danbooru.donmai.us/" in url):
            return web_retriever.WebRetriever().retrieve_danbooru(url, no_pages, wait)
        if("https://rule34.xxx/" in url):
            return web_retriever.WebRetriever().retrieve_r34(url, no_pages, wait)
        if("https://hitomi.la/" in url):
            return web_retriever.WebRetriever().retrieve_hitomi_la(url, wait, no_pages)
        raise Exception("We couldn't find a proper link here, matey :(")
    
    def _scrap_posts(self,url,html_list=[]):
        """Discriminates between domains to call the apropiate scraper. Returns a list of touples(gallery_name,list_of_post_urls)"""
        if("https://e-hentai.org/" in url):
            post_urls = []
            for html in html_list:
                temporal_list = []
                gallery_name = ""
                temporal_list = scraper.Scraper.scrap_ehentai(self, html)
                gallery_name = temporal_list[0]
                post_urls += temporal_list[1]
            print ("Found: "+str(len(post_urls))+" Image Posts")
            return [gallery_name,post_urls]
        
        if("danbooru.donmai.us/" in url):
            post_urls = []
            for html in html_list:
                temporal_list = []
                gallery_name = ""
                temporal_list += scraper.Scraper.scrap_danbooru(self, html)
                gallery_name = temporal_list[0]
                post_urls += temporal_list[1]
            print ("Found: "+str(len(post_urls))+" Image Posts")
            return [gallery_name,post_urls]
        if("https://rule34.xxx/" in url):
            post_urls = []
            for html in html_list:
                temporal_list = []
                gallery_name = ""
                temporal_list += scraper.Scraper.scrap_r34(self, html)
                gallery_name = temporal_list[0]
                post_urls += temporal_list[1]
            print ("Found: "+str(len(post_urls))+" Image Posts")
            return [gallery_name,post_urls]
        if("https://hitomi.la/" in url):
            #This step is also skipped.
            return (scraper.Scraper.scrap_hitomi(self, html_list[0]),html_list)
        raise Exception("Couldn't get any post from your url")
    
    def _check_url_domain(self,url):
        """Validates a webpage's domain in url for a supported site"""
        supported_domains = ["e-hentai.org","danbooru.donmai.us","rule34.xxx","hitomi.la"]
        
        for domain in supported_domains:
            if url.find(domain) > -1:
                return
        raise Exception("Not a supported website found")
    
    def create_output_dir(self,path,dir_name):
        """Creates a directory according to path and folder name"""
        try:
            #This bullshit right here is to remove character that arent supported in directory names. I got lazy and copy pasted themselves :P
            dir_name = dir_name.replace("|"," ").replace("<"," ").replace(">", " ").replace(":", " ").replace("\"", " ").replace("\\", " ")
            dir_name = dir_name.replace("/"," ").replace("?"," ").replace("*", " ")
            os.makedirs(path+"\\"+dir_name.strip())
            return path+"\\"+dir_name.strip()
        except OSError as e:
            return path+"\\"+dir_name.strip()
        
@click.command()
@click.option('-b',help="Path to a txt with multiple urls as: url,pages. One per line."+
              " This option overrides -u and -p.")
@click.option('-u',help="Gallery (or reader) url")
@click.option('-p',help="Number of pages",default=1)
@click.argument("output_path")
@click.option('-w',help="Wait time between downloads, defaut is 1.0 sec",default=1.0)
def clickerino(b, u, p, output_path, w):
    """Suported sites include: ehentai.org, r34.xxx,
    danbooru.donmai and hitomi.la/reader.
    \nWARNING NO.1: For hitomi.la, a page from the reader of the
    desired gallery must be given, no need to set -p."""
    if u is None and b is None:
        click.echo("Hey, there is no url, nor text file with links here!")
        exit()
        
    if b is not None:
        click.echo(b)
    else:
        core = HCore()
        core.user_input(u, p, output_path, w)

if __name__ == '__main__':
    clickerino()