'''
Created on 23/02/2018

@author: XrossFox
'''

from hscrap.global_vars import GlobalVars
from urllib.request import Request, urlopen, urlretrieve
import time
class WebRetriever():
    '''
    Class that contains page retrieval methods for web items.
    '''
        
    def retrieve_ehentai(self,url,pages,wait=1):
        """Retrieves page/s from ehentai.org."""
        #request data for retrieval
        html_data = list()
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        for l_pages in range(pages):
            if l_pages > 0:
                req = Request(url+'?p='+str(l_pages),headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+url+'?p='+str(l_pages)+" page: "+str(l_pages+1))
            else:
                req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+url+" page: "+str(l_pages+1))
            data = urlopen(req).read()
            text = data.decode('utf-8')
            html_data.append(text)
            
            time.sleep(wait)
        return html_data
    
    def retrieve_danbooru(self,url,pages,wait=1):
        """Retrieves page/s from Danbooru."""
        #request data for retrieval
        html_data = list()
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        for l_pages in range(pages):
            if l_pages > 0:
                mid_url = "?page={}&".join(url.split(sep="?")).format(l_pages+1)
                req = Request(mid_url,headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+mid_url+" page: "+str(l_pages+1))
            else:
                req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+url+" page: "+str(l_pages+1))
            data = urlopen(req).read()
            text = data.decode('utf-8')
            html_data.append(text)
            time.sleep(wait)
        return html_data

    def retrieve_r34(self,url,pages,wait=1):
        """Retrieves page/s from Danbooru."""
        #request data for retrieval
        html_data = list()
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        for l_pages in range(pages):
            if l_pages > 0:
                mid_url = url+"&pid="+str(42*l_pages)
                req = Request(mid_url,headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+mid_url)
            else:
                mid_url = url+"&pid="+str(42*l_pages)
                req = Request(mid_url,headers={'User-Agent': 'Mozilla/5.0'})
                print("Retrieved: "+url)
            data = urlopen(req).read()
            text = data.decode('utf-8')
            html_data.append(text)
            time.sleep(wait)
        return html_data    
    
        