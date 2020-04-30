from konlpy.tag import Okt
import csv
import pandas
import os
import time
import re
import logging
import pickle
import json
from threading import Thread
import jpype

class Preprocessor():
    def __init__(self):
        self.keyword = None
        self.media = None
        self.MEDIA_MUSINSA = "musinsa"
        self.MEDIA_INSTAGRAM = "instagram"

        ##파일 경로  
        self.folder_filepath = 'polls/module/data'
        self.prepro_filename = '/preprocessed_%s.csv'
        self.stop_words_filename = '/stopword.csv'
        self.category_filename = '/category.csv'
        self.raw_musinsa_filepath = 'polls/module/Crawler/rawdata/contents_musinsa.csv'
        self.raw_insta_filepath = 'polls/module/Crawler/rawdata/contents_instagram.csv'
       
        ##테스트 파일 경로 
        # self.folder_filepath = './data'
        # self.raw_musinsa_filepath = './Crawler/rawdata/contents_musinsa.csv'
        # self.raw_insta_filepath = './Crawler/rawdata/contents_instagram.csv'
        
        self.logger = self.settingLogger()

        self.createFile()

    def createFile(self):
        ##전처리 데이터 폴더 생성
        if os.access(self.folder_filepath,os.F_OK) == False:
            os.mkdir(self.folder_filepath)

        ## 전처리 데이터 파일 생성
        filepath = filepath = self.folder_filepath + self.prepro_filename % self.MEDIA_MUSINSA
        if os.access(filepath,os.F_OK) == False:
            new_data = {'keyword':[],'text':[],'date':[],'category':[]}
            df = pandas.DataFrame(new_data,columns=['keyword','text','date','category'])
            df.to_csv(filepath,index=False, encoding='utf-8')

        filepath = filepath = self.folder_filepath + self.prepro_filename % self.MEDIA_INSTAGRAM
        if os.access(filepath,os.F_OK) == False:
            new_data = {'keyword':[],'text':[],'date':[],'category':[]}
            df = pandas.DataFrame(new_data,columns=['keyword','text','date','category'])
            df.to_csv(filepath,index=False, encoding='utf-8')
        
    def settingLogger(self):
        # 로거 생성
        logger = logging.getLogger('preprocessing.log')
        logger.setLevel(logging.DEBUG)

        # 로그포맷팅
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # 스트림 핸들러
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.DEBUG)
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)

        return logger
    
    def set_keyword(self,keyword):
        self.keyword = keyword
    
    def get_keyword(self):
        return self.keyword

    def set_media(self,media):
        self.media = media
    
    def get_media(self):
        return self.media

    def excute_preprocessing(self):
        ##예외처리
        if(self.keyword == None):
            print("Please set keyword")
            return
        if(self.media == None):
            print("Please set media")
            return 

        ##raw data 파일경로 설정
        if(self.media == self.MEDIA_MUSINSA):
            filepath = self.raw_musinsa_filepath
        elif(self.media == self.MEDIA_INSTAGRAM):
            filepath = self.raw_insta_filepath

        # raw data
        raw_data = pandas.read_csv(
            filepath, index_col=False, encoding='utf-8')
        raw_data = raw_data[raw_data['keyword'] == self.keyword]
        raw_data = raw_data.dropna(how="any")
        raw_data = raw_data.reset_index(drop=True)
        #raw_data = raw_data[raw_data.index <= 1000]  # 데이터 수 조절
        #raw_data
        
        if len(raw_data) == 0 :
            return "zeroData"

        # stopword ---> 나중에 인스타도 불용어 추가해야함 
        filepath = self.folder_filepath + self.stop_words_filename
        df = pandas.read_csv(filepath,index_col=False, encoding='utf-8')
        stop_words = list(df['word'])

        # category data
        filepath = self.folder_filepath + self.category_filename
        category_data = pandas.read_csv(filepath,index_col=False, encoding='utf-8')
        
        ##스레드 작업 범위 설정
        start = raw_data.index[0]
        end = raw_data.index[-1]
        nlines = len(raw_data)

        ##전처리 작업 병렬 수행
        okt = Okt()
        result = [] ##전처리 결과
        try:
            self.logger.debug("Preprocessing Start - Data length : %s" % nlines)
            t1 = Thread(target=self.preprocessing_parallel,
                        args=(start, start+int(nlines/2), raw_data, okt, result,category_data,stop_words))
            t2 = Thread(target=self.preprocessing_parallel, 
                        args=(start+int(nlines/2), end, raw_data, okt, result,category_data,stop_words))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except KeyboardInterrupt:
            pass
        except Exception:
            pass
        finally:
            self.save_data(result)
            self.logger.debug("Preprocessing Complete")
            self.logger.debug("\t Keyword %s" % self.keyword)
            self.logger.debug("\t Complete data length %s" % len(result))

    # 병렬 데이터 전처리
    def preprocessing_parallel(self,start, end, raw_data, okt, result,category_data,stop_words=[]):
        # 함수의 인자는 다음과 같다.
        # 병렬 수행함으로 작업 처리 범위 인덱스 지정
            # start : 전처리할 로우 데이터 시작 인덱스
            # end : 전처리할 로우 데이터 마지막 인덱스
        # review : 로우 데이터.
        # okt : okt 객체를 반복적으로 생성하지 않고 미리 생성후 인자로 받는다.
        # result : 전처리 결과 저장할 리스트.
        # remove_stopword : 불용어를 제거할지 선택 기본값은 False
        # stop_word : 불용어 사전은 사용자가 직접 입력해야함 기본값은 비어있는 리스트

        jpype.attachThreadToJVM()

        #전처리할 텍스트 한글 및 공백 문자 제외 모두 제거
        # okt 객체를 활용해서 형태소 단위로 나눈다.
        review_text = raw_data['text']
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        review_text = [hangul.sub('',str(review)) for review in review_text]
        review_text = [review.strip() for review in review_text]
        review_text = [okt.morphs(str(review_text[i])) for i in range(start, end) if review_text[i] != '']
        
        ##카테고리 데이터
        category_colors = list(category_data['색'].dropna())
        category_price = list(category_data['가격'].dropna())
        category_size = list(category_data['사이즈'].dropna())
        
        ##불용어 제거 및 카테고리 판단
        index = start
        for review in review_text:
            ##불용어 제거
            word_review = [
                token for token in review if not token in stop_words]
            
            ##카테고리 판단
            category = "None"
            for token in word_review:
                if token in category_colors:
                    category = "color"
                elif token in category_price:
                    category = "price"
                elif token in category_size:
                    category = "size"
            
            word_review = ' '.join(word_review)
            if word_review != '':
                result.append([self.keyword,word_review,raw_data['date'].ix[index],category])

            index+=1
        return
    
    ##전처리 데이터 파일 저장
    def save_data(self,result):
        self.logger.debug("Save data")

        if(self.get_media() == self.MEDIA_MUSINSA):
            filepath = self.folder_filepath + self.prepro_filename % self.MEDIA_MUSINSA
        elif(self.get_media() == self.MEDIA_INSTAGRAM):
            filepath = self.folder_filepath + self.prepro_filename % self.MEDIA_INSTAGRAM

        with open(filepath,'a',encoding="utf-8",newline='') as f:
            wr = csv.writer(f)
            for data in result:
                wr.writerow(data)

        df = pandas.read_csv(filepath,encoding='utf-8',index_col=False)
        df.drop_duplicates().to_csv(filepath,index=False,encoding='utf-8')

if __name__ == '__main__':
    prepro = Preprocessor()
    prepro.set_keyword("청바지") ##나중에는 지워야 할 것
    prepro.set_media(prepro.MEDIA_MUSINSA)

    start_time = time.time()
    prepro.excute_preprocessing()
    print("time : ", (time.time()-start_time))