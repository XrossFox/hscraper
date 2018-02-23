'''
Created on 21/02/2018

@author: David
'''
class GlobalVars():
    def __init__(self):
        self._url = ""
        self._no_pages = 0
        self._out_path = ""
        
    def set_url(self,url):
        """Sets url attribute"""
        if isinstance(url, str):
            self._url = str(url)
        else:
            raise Exception("Not an str instance")
         
    def get_url(self):
        """return url attribute"""
        return self._url
         
                 
    def set_no_pages(self,no_pages):
        """Sets no_pages attribute"""
        if isinstance(no_pages, int):
            self._no_pages = int(no_pages)
        else:
            raise Exception("Not an int instance")
    
    def get_no_pages(self):
        """Returns no_pages attribute value"""
        return self._no_pages

    def set_out_path(self,out_path):
        """Sets out_path attribute"""
        if isinstance(out_path, str):
            self._out_path = str(out_path)
        else:
            raise Exception("Not an str instance")
    
    def get_out_path(self):
        """Returns no_pages attribute value"""
        return self._out_path