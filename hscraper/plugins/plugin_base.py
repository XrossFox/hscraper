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
    def start(self, url, pages, skip_from, wait, retry, wait_retry, output):
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

        path = path.replace("\\","/")
        path = re.sub(r"[<>\"|\?\*^]+", "", path)
        name = re.sub(r"[<>:\"\\|\?\*^]+", "", name)
        
        if not path.endswith("/"):
            path = path+"/"
        
        if not os.path.exists(path+name):
            os.makedirs(path+name)

        return path+name
            
    def write_to(self, path, name, payload):
        """
        Writes a stream of bytes (payload) to a path and a name.
        """
        path = path.replace("\\","/")
        path = re.sub(r"[<>\"|\?\*^]+", "", path)
        name = re.sub(r"[<>:\"\\|\?\*^]+", "", name)
        
        if not path.endswith("/"):
            path = path+"/"
        
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
    
    def gen_string_header(self, url, pages, skip_from, wait, retry, wait_retry, output):
        """
        Returns message that has information about this particular run.
        """
        if not skip_from:
            skip_from = 1
        return ("="*70+"\n\n{0:20}:{1}\n{2:20}:{3}\n{4:20}:{5}\n{6:20}:{7}\n{8:20}:{9}\n{10:20}:{11}\n{12:20}:{13}\n".format(
            "Url",url[:50],"Pages",pages,"From Page",skip_from,"Wait Time",wait,
            "Retries",retry,"Wait Between Retries",wait_retry,"Ouput directorty",output
            ))
    
    def gen_invalid_url_string(self,url):
        """
        Returns a message when an invalid url is found.
        """
        return ("\n"+">"*4+"Invalid Url in: {}".format(url)+"\n")
    
    def gen_valid_url_string(self,url):
        """
        Returns a message when a valid url is found.
        """
        return ("Valid Url in: {}".format(url))
    
    def gen_scraping_page_string(self,url):
        """
        Returns a message about the current page that is being scraped.
        """
        return ("\n"+"+"*70+"\nCurrent page: {}\n".format(url)+"-"*70+"\n")
    
    def gen_downloading_string(self, path, name):
        """
        Returns a message about the current image that is being downloaded. 
        """
        return ("Downloading: {}/{}".format(path,name))
        
    def gen_foot_string(self, downloaded, pages, skipped, failed, list_failed):
        """
        Returns a message about the results of a particular run.
        """
        l_s = ""
        for s in list_failed:
            l_s += s+"\n"
        
        return ("="*70+"\n{0:20}:{1}\n{2:20}:{3}\n{4:20}:{5}\n{6:20}:{7}\n{8:20}\n{9}".format(
            "Downloaded",downloaded,"Pages",pages,"Skipped",skipped,"Failed",failed,":",l_s)+"="*70)
        
    def gen_page_not_found_string(self, page_url):
        """
        Returns a message about the page that couldnt be found
        """
        return ("Couldnt find page: {}".format(page_url))

    def gen_img_not_found_string(self, img_url):
        """
        Returns a message about the image that couldnt be found
        """
        return ("Couldnt find image: {}".format(img_url))