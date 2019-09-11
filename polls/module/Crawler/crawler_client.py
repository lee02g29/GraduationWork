##장고에서 이런식으로 사용할 것!!!

import requests

class CrawlerClient():
    def __init__(self):
        self.keyword = None
        self.media = None
    
    def setKeyword(self,keyword):
        self.keyword = keyword

    def setMedia(self,media):
        self.media = media

    def get(self,url):
        #params = {'param1':self.media, 'param2':self.keyword}
        requests.get(url)


#if __name__ == '__main__':
 #   pass
    ##검색 키워드
    #keyword = '청바지'   

    ##크롤링할 매체
    #media = crawler_server.MEDIA_INSTAGRAM
    #media = crawler_server.MEDIA_MUSINSA  

    #url =  'http://127.0.0.1:5000/save/%s/%s' % (media,keyword) 
    #requests.get(url)   ##GET 요청