import os
import requests
import re
from time import sleep
from abc import ABC, abstractmethod


class PluginBase(ABC):
    '''
    Base class for scraper plug-ins.
    '''
    @abstractmethod
    def start(self, url, pages, skip_from, skip_to, wait, retry, wait_retry, output):
        """
        Abstract method for control flow
        """
        pass
    
    @abstractmethod
    def gen_gal_name(self,url):
        pass
    
    @abstractmethod
    def validate_url(self,url):
        pass
    
    @abstractmethod
    def scrap_for_pages(self, url, pages, skip_from=None):
        """
        Abstract method that scraps html code for pages
        """
        pass
    
    @abstractmethod
    def scrap_for_posts(self, url, wait, retry, wait_retry):
        """
        Abstract method that scraps html code for posts
        """
        pass
    
    @abstractmethod
    def scrap_for_images(self, url, wait, retry, wait_retry):
        """
        Abstract method that scraps html code for images
        """
        pass
    
    def create_dir(self, path, name):
        """
        Creates output directory to store downloaded galleries. This test requires an already existing directory
        c:\test
        """
        print(path+name) 
        path = path.replace("\\","/")
        path = re.sub(r"[<>\"|\?\*^]+", "", path)
        name = re.sub(r"[<>:\"\\|\?\*^]+", "", name)
        
        if not path.endswith("/"):
            path = path+"/"
        
        if not os.path.exists(path+name):
            os.makedirs(path+name)
        print(path+name) 
        return path+name
            
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
        
    
    def get_request(self, url, wait, retry, wait_retry, cookies=None):
        """
        Sends an http request to the given url. returns a dictionary with 3 keys:
        
        payload: the response
        responce_code: self explanatory
        retry: how many tries were done
        
        You can set number of retries and time between retries with given parameters.
        
        You can also send a dictionary as cookies.
        """
        
    
        headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        #cookies = cookies
        res = {'retry':retry, 'response_code':404, 'payload':None}
        
        for n_retry in range(retry):
            try:
                if cookies:
                    req = requests.get(url, headers=headers, cookies=cookies)
                else:
                    req = requests.get(url, headers=headers)
                
                res['payload'] = req.content
                res['response_code'] = req.status_code
                res['retry'] = n_retry + 1
                break
                
            except Exception as w:
                print("Error downloading : {}\nRetrying in: {}".format(url, wait_retry))
                res['payload'] = None
                res['response_code'] = 404
                res['retry'] = n_retry + 1 
                sleep(wait_retry)
                
        sleep(wait)
        return res