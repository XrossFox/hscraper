'''
Created on 23/02/2018

@author: XrossFox
'''

from urllib.request import Request, urlopen
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
        """Retrieves page from Hitomi.la reader, only one is needed, since it technically has no pagination.
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
    
    def retrieve_web_page(self,post_url,wait=1):
        """Retrieves a single html doc from the internet"""
        req = Request(post_url,headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read()
        html = data.decode('utf-8')
        print("Looking for: "+post_url)
        time.sleep(wait)
        return html
    
    def retrieve_image(self,img_url,path,wait=1):
        retry = 3
        while retry > 0:
            try:
                req = Request(img_url,headers={'User-Agent': 'Mozilla/5.0'})
                data = urlopen(req).read()
                img_name = (img_url.split("/")[-1][:50]) if len(img_url.split("/")[-1])>50 else img_url.split("/")[-1]
                img_extension = "."+img_url.split("/")[-1].split(".")[-1]
                if "?" in img_extension:
                    img_extension = img_extension.split("?")[0]
                    img_extension = img_extension.replace("?","_")
                    img_name = img_name.replace("?","_")
                with open(path+"\\"+img_name+img_extension, 'wb') as outfile:
                    print("Saving to: "+path+"\\"+img_name+img_extension)
                    outfile.write(data)
                break
            except Exception as e:
                print(e)
                print("Error, Retrying...")
                retry -= 1
                continue
        time.sleep(wait)