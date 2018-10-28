import requests
from fake_useragent import UserAgent
from time import sleep

class PluginBase(object):
    '''
    Base class for scraper plug-ins.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def get_html(self, url, wait, retry, wait_retry):
        ua = UserAgent(cache=False)
        headers = {"User-Agent" : ua.random}
        res = {'retry':retry, 'response_code':404, 'payload':None}
        
        for n_retry in range(retry):
            try:
                
                req = requests.get(url, headers=headers)
                res['payload'] = req.text
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
    
        