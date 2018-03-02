'''
Created on 21/02/2018

@author: David
'''
import os
import errno
from hscrap.global_vars import GlobalVars
class HCore():
    
    def user_input(self,url,no_pages,output_path = os.path.dirname(__file__)+"\\"):
        """Receives url, number of pages and optional output path. Starts the process."""
        g_ref = GlobalVars()
        
        #check url
        g_ref.set_url(url)
        self._check_url_domain(url)
        g_ref.set_no_pages(no_pages)
        return g_ref
    
    def _check_url_domain(self,url):
        """Validates a webpage's domain in url for a supported site"""
        supported_domains = ["e-hentai.org","danbooru.donmai.us","rule34.xxx","hitomi.la"]
        
        for domain in supported_domains:
            if url.find(domain) > 0:
                return
        raise Exception("Not a supported site found")
    
    def create_output_dir(self,path,dir_name):
        """Creates a directory according to path and folder name"""
        try:
            #This bullshit right here is to remove character that arent supported in directory names. I got lazy and copy pasted themselves :P
            dir_name = dir_name.replace("|"," ").replace("<"," ").replace(">", " ").replace(":", " ").replace("\"", " ").replace("\\", " ")
            dir_name = dir_name.replace("/"," ").replace("?"," ").replace("*", " ")
            os.makedirs(path+dir_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise