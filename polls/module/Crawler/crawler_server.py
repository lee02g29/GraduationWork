from flask import Flask
from instagramCrawler import InstagramCrawler
from musinsaCrawler import MusinsaCrawler
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import os
import logging

##크롤러서버
    ##GET방식으로 통신. URL에 검색할 키워드 데이터를 넘겨줌
    ##검색한 키워드 받으면 리스트에 추가
        ##keywords_musinsa - 무신사 키워드 리스트
        ##keywords_insta - 무신사 키워드 리스트
    ##스케줄러이용 주기적으로 크롤링 함수 실행
        ##crawling_instagram() - 인스타그램
        ##crawling_musinsa() - 무신사
        ##키워드 리스트에 저장된 키워드를 크롤링

    ##클라이언트 서버 연결 방법
        ##GET 방식 통신
        ##URL = 서버IP주소/save/<media>/<data>
        ##<media> 이 부분에 검색 매체가 들어감 (여기서 크롤러 선택)
        ##<data> 이 부분에 검색할 키워드가 들어감
        ##ex) http://서버IP주소/save/musinsa/청바지

MEDIA_MUSINSA = "musinsa"
MEDIA_INSTAGRAM = "instagram"    

keywords_musinsa = []
keywords_insta = []

##로그설정
logger = None
def set_logs(logger_name,filepath):
    global logger

    ##로깅파일 생성
    if os.access('./logging',os.F_OK) == False:
        os.mkdir('./logging')   
        
    ##로거 생성
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
        
    ##로그포맷팅
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
    ##파일 핸들러
    fileHandler = logging.FileHandler(filepath)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
        
    ##스트림 핸들러
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
        
    ##핸들러 등록
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

##DB 생성
conn = None
def create_DB():
    global conn

    DB_filepath = './crawler.db'
    if os.access(DB_filepath,os.F_OK) == False:
        conn = sqlite3.connect(DB_filepath)
        curs = conn.cursor()
        curs.execute('create table keyword(media, word)')
    conn = sqlite3.connect(DB_filepath)

##DB에 저장된 키워드 로드
def load_keywords():
    global logger
    global conn
    global keywords_insta
    global keywords_musinsa

    curs = conn.cursor()

    sql = 'select media, word from keyword'
    rows = curs.execute(sql)
    for row in rows:
        if row[0] == MEDIA_MUSINSA:
            keywords_musinsa.append(row[1])    
        if row[0] == MEDIA_INSTAGRAM:
            keywords_insta.append(row[1])
    
    sql = 'delete from keyword'
    curs.execute(sql)
    conn.commit()

    logger.debug("keyword load - musinsa : %s  insta : %s" % (len(keywords_musinsa),len(keywords_insta)))

##DB에 키워드 저장
def save_keywords():
    global logger
    global conn
    global keywords_insta
    global keywords_musinsa

    curs = conn.cursor()

    sql = "insert into keyword(media,word) values(?,?)"
    for word in keywords_musinsa:    
        curs.execute(sql,(MEDIA_MUSINSA,word))
    for word in keywords_insta:
        curs.execute(sql,(MEDIA_INSTAGRAM,word))
    
    conn.commit()
    logger.debug("keyword save - musinsa : %s  insta : %s" % (len(keywords_musinsa),len(keywords_insta)))

##크롤링 함수 - 인스타그램
is_done_insta = True
def crawling_instagram():
    global logger
    global keywords_insta
    global is_done_insta

    ##예외처리
    if is_done_insta == False:
        return
    if len(keywords_insta) == 0:
        return

    ##리스트에 저장된 키워드 크롤링
    logger.debug("Crawling Start - instagram : %s" % (len(keywords_insta)))
    is_done_insta = False
    crawler = InstagramCrawler()
    for i in range(0,len(keywords_insta)):
        keyword = keywords_insta.pop(i)
        logger.debug("Crawling - instagram - keyword : %s" % (keyword))

        crawler.set_keyword(keyword)
        if crawler.get_links():
            crawler.get_contents()
    is_done_insta = True
    logger.debug("Crawling Complete - instagram")

##크롤링 함수 - 무신사
is_done_musinsa = True
def crawling_musinsa():
    global logger
    global keywords_musinsa
    global is_done_musinsa

    ##예외처리
    if is_done_musinsa == False:
        return
    if len(keywords_musinsa) == 0:
        return

    ##리스트에 저장된 키워드 크롤링
    logger.debug("Crawling Start - musinsa : %s" % (len(keywords_musinsa)))
    is_done_musinsa = False
    crawler = MusinsaCrawler()
    for i in range(0,len(keywords_musinsa)):
        keyword = keywords_musinsa.pop(i)
        logger.debug("Crawling - musinsa - keyword : %s" % (keyword))

        crawler.set_keyword(keyword)
        crawler.get_links()
        crawler.get_contents()
    is_done_musinsa = True
    logger.debug("Crawling Complete - musinsa")

app = Flask(__name__)

##홈페이지에서 검색 키워드 GET방식 통신
@app.route('/save/<media>/<word>' ,methods=['GET'])
def get_Keyword(media,word):
    global keywords_musinsa
    global keywords_insta

    ##크롤링할 키워드 리스트에 저장
    if media == MEDIA_INSTAGRAM:
        keywords_insta.append(word)
    elif media == MEDIA_MUSINSA:
        keywords_musinsa.append(word)

    return word

if __name__ == "__main__":
    INTERVAL_TIME = 2
    try:
        set_logs('Crawler_Server_log','./logging/logfile_CrawlerServer.log')

        ##DB 생성 및 연결 후 DB에 저장된 크롤링할 키워드 로드
        create_DB()
        load_keywords()

        ##스케줄러 이용 - 백그라운드에서 주기적으로 인스타/무신사 크롤링 실행
            ##2초에 한번씩 크롤링 함수 실행 -- 테스트이므로 나중에는 시간 조절 필요
        scheduler = BackgroundScheduler() 
        job = scheduler.add_job(crawling_instagram, 'interval', seconds=INTERVAL_TIME) 
        job = scheduler.add_job(crawling_musinsa, 'interval', seconds=INTERVAL_TIME) 
        scheduler.start() 

        ##서버 실행
        app.run()

        ##아직 크롤링 하지 못한 키워드 DB에 저장
        save_keywords()
        conn.close()

    except KeyboardInterrupt:
        save_keywords()
        conn.close()