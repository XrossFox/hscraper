import os
import requests
import re
from fake_useragent import UserAgent
from time import sleep
from abc import ABC, abstractmethod


class PluginBase(ABC):
    '''
    Base class for scraper plug-ins.
    '''
    @abstractmethod
    def start(self, url, pages, skip_pages, wait, retries, wait_retries, output):
        """
        Abstract method for control flow
        """
        pass
    
    @abstractmethod
    def validate_url(self,url):
        pass
    
    @abstractmethod
    def scrap_for_pages(self):
        """
        Abstract method that scraps html code for pages
        """
        pass
    
    @abstractmethod
    def scrap_for_posts(self):
        """
        Abstract method that scraps html code for posts
        """
        pass
    
    @abstractmethod
    def scrap_for_images(self):
        """
        Abstract method that scraps html code for images
        """
        pass
    
    def create_dir(self, path):
        """
        Creates output directory to store downloaded galleries.
        """
        
        path = re.sub(r"[<>:\"\\|\?\*^]+", "", path)
         
        if not os.path.exists(path):
            os.makedirs(path)
            
    def write_to(self, path, name, payload):
        """
        Writes a stream of bytes (payload) to a path and a name.
        """
        path = re.sub(r"[<>:\"\\|\?\*^]+", "", path)
        name = re.sub(r"[<>:/\"\\|\?\*^]+", "", name)
        
        if not path:
            path="."
        
        try:
            file = open(path+"/"+name, "wb")
            file.write(payload)
            file.close()
        except Exception as w:
            print(w)
            print("Couldn't write: {}".format(path+"/"+name))
        
    
    def get_request(self, url, wait, retry, wait_retry, **cookies):
        """
        Sends an http request to the given url. returns a dictionary with 3 keys:
        
        payload: the response
        responce_code: self explanatory
        retry: how many tries were done
        
        You can set number of retries and time between retries with given parameters.
        
        You can also send a dictionary as cookies.
        """
        
        ua = UserAgent(cache=False)
        headers = {"User-Agent" : ua.random}
        cookies = cookies
        res = {'retry':retry, 'response_code':404, 'payload':None}
        
        for n_retry in range(retry):
            try:
                req = requests.get(url, headers=headers, cookies=cookies)
                res['payload'] = req.content
                res['response_code'] = req.status_code
                res['retry'] = n_retry + 1
                break
                
            except Exception as w:
                res['payload'] = None
                res['response_code'] = 404
                res['retry'] = n_retry + 1 
                sleep(wait_retry)
                
        sleep(wait)
        return res