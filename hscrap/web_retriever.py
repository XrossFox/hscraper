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

    def __init__(self, globalatts):
        '''
        Constructor
        '''
        if not isinstance(globalatts, GlobalVars):
            raise Exception("Not an instance of GlobalVars")
        self.globalatts = globalatts
        
    def retrieve_ehentai(self):
        """Recupera la/s pagina/s de la publicacion."""
        #request data for retrieval
        html_data = list()
        req = Request(self.globalatts.get_url(),headers={'User-Agent': 'Mozilla/5.0'})
        for l_pages in range(self.globalatts.get_no_pages()):
            if l_pages > 0:
                req = Request(self.globalatts.get_url()+'?p='+str(l_pages),headers={'User-Agent': 'Mozilla/5.0'})
            else:
                req = Request(self.globalatts.get_url(),headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            text = data.decode('utf-8')
            html_data.append(text)
            print("Retrieved: "+self.globalatts.get_url()+" page: "+str(l_pages+1))
            time.sleep(self.globalatts.get_wait_time())
        return html_data
    
        