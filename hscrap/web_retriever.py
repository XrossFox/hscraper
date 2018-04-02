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
        """Retrieves page/s from ehentai.org as a list."""
        #request data for retrieval
        url_lists = list()
        for l_pages in range(pages):
            if l_pages > 0:
                url_lists.append(url+'?p='+str(l_pages))
            else:
                url_lists.append(url)
        return self._retrieve_web_pages(url_lists)
    
    def retrieve_danbooru(self,url,pages,wait=1):
        """Retrieves page/s from Danbooru as a list."""
        #request data for retrieval
        url_lists = list()
        for l_pages in range(pages):
            if l_pages > 0:
                url_lists.append("?page={}&".join(url.split(sep="?")).format(l_pages+1))
            else:
                url_lists.append(url)
        return self._retrieve_web_pages(url_lists)
    
    def retrieve_r34(self,url,pages,wait=1):
        """Retrieves page/s from r34 as a list."""
        #request data for retrieval
        url_lists = list()
        for l_pages in range(pages):
            if l_pages > 0:
                url_lists.append(url+"&pid="+str(42*l_pages))
            else:
                url_lists.append(url+"&pid="+str(42*l_pages)) 
        return self._retrieve_web_pages(url_lists)
    
    def retrieve_hitomi_la(self,url,wait=1,pages=1):
        """Retrieves page from Hitomi.la, only one is needed, since it technically has no pagination.
        Also returns a list for consistency"""
        #request data for retrieval
        url_lists = [url]
        return self._retrieve_web_pages(url_lists)
        
    def _retrieve_web_pages(self,url_list=[],wait=1):
        '''Retrieves a list of htmls from a list of urls. Not meant to be called directly, but as a helper for
        methods above'''
        html_data = list()
        for url in url_list:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            html = data.decode('utf-8')
            html_data.append(html)
            print("Retrieved: "+url)
            time.sleep(wait)
        return html_data
    
    
    