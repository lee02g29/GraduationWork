import pandas
import csv
import os
import re
import logging
import time
from konlpy.tag import Komoran
from threading import Thread
import jpype

class AssocitatedAnalysis():
    def __init__(self):
        self.keyword = None
        self.media = None
        self.MEDIA_MUSINSA = "musinsa"
        self.MEDIA_INSTAGRAM = "instagram"
        self.yearlist = []
        
        self.folder_filepath = 'polls/module/data'
        self.associate_filename = '/associated_%s.csv'
        self.raw_musinsa_filepath = 'polls/module/Crawler/rawdata/contents_musinsa.csv'
        self.raw_insta_filepath = 'polls/module/Crawler/rawdata/contents_instagram.csv'
        self.stop_words_filename = '/associate_stopwords.csv'
        self.user_dic_filepath = '/user_dic.txt'

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
        filepath = self.folder_filepath + self.associate_filename % self.MEDIA_MUSINSA
        if os.access(filepath,os.F_OK) == False:
            new_data = {'keyword':[],'words':[],'date':[]}
            df = pandas.DataFrame(new_data,columns=['keyword','words','date'])
            df.to_csv(filepath,index=False, encoding='utf-8')

        filepath = self.folder_filepath + self.associate_filename % self.MEDIA_INSTAGRAM
        if os.access(filepath,os.F_OK) == False:
            new_data = {'keyword':[],'words':[],'date':[]}
            df = pandas.DataFrame(new_data,columns=['keyword','words','date'])
            df.to_csv(filepath,index=False, encoding='utf-8')

    def settingLogger(self):
        # 로거 생성
        logger = logging.getLogger('associate.log')
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
        if self.media == self.MEDIA_INSTAGRAM:
            self.date_pattern = "%s-"
        elif self.media == self.MEDIA_MUSINSA:
            self.date_pattern = "%s."
        else :
            self.media = None
            
    def get_media(self):
        return self.media

    ##현재 저장되어있는 리뷰 연도리스트 반환
    def get_year_list(self):
        if(self.media == self.MEDIA_MUSINSA):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_MUSINSA
        elif(self.media == self.MEDIA_INSTAGRAM):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_INSTAGRAM

        now = time.localtime() ##현재날짜
        for year in range(now.tm_year,now.tm_year-3,-1): ##현재 연도로부터 3년간 데이터 존재하는지 
            df = pandas.read_csv(filepath,encoding='utf-8',index_col=False)
            df = df[df['keyword'] == self.keyword]
            df = df.dropna(how="any")
            pattern = self.date_pattern % (str(year))
            df = df.ix[df['date'].str.startswith(pattern),:]
            if(len(df) != 0):
                self.yearlist.append(year)
        return self.yearlist
        
    ##전처리 함수 -->병렬수행
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
        raw_data = pandas.read_csv(filepath, index_col=False, encoding='utf-8')
        raw_data = raw_data[raw_data['keyword'] == self.keyword]
        raw_data = raw_data.reset_index(drop=True)

        if len(raw_data) == 0 :
            return 

        # stopword --> 연관어 분석용 
        filepath = self.folder_filepath + self.stop_words_filename
        df = pandas.read_csv(filepath,index_col=False, encoding='utf-8')
        stop_words = [str(word) for word in df['stopword']]

        ##스레드 작업 범위 설정
        start = raw_data.index[0]
        end = raw_data.index[-1]
        nlines = len(raw_data)

        ##형태소 분석객체
            ##사용자 사전을 추가하도록 함
        komo = Komoran(userdic=self.folder_filepath+self.user_dic_filepath)

        ##전처리 작업 병렬 수행
        result = [] ##전처리 결과
        try:
            self.logger.debug("Preprocessing Start - Data length : %s" % nlines)
            t1 = Thread(target=self.preprocessing_parallel,
                        args=(start, start+int(nlines/2), raw_data, komo, result, True, stop_words))
            t2 = Thread(target=self.preprocessing_parallel, args=(
                start+int(nlines/2), end, raw_data, komo, result, True, stop_words))
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
    

    # 병렬 데이터 전처리 연산 함수
    def preprocessing_parallel(self,start, end, raw_data,komo, result, remove_stopwords=False, stop_words=[]):
        # 함수의 인자는 다음과 같다.
        # 병렬 수행함으로 작업 처리 범위 인덱스 지정
            # start : 전처리할 로우 데이터 시작 인덱스
            # end : 전처리할 로우 데이터 마지막 인덱스
        # review : 로우 데이터.
        # komo : komoran 객체를 반복적으로 생성하지 않고 미리 생성후 인자로 받는다.
        # result : 전처리 결과 저장할 리스트.
        # remove_stopword : 불용어를 제거할지 선택 기본값은 False
        # stop_word : 불용어 사전은 사용자가 직접 입력해야함 기본값은 비어있는 리스트

        jpype.attachThreadToJVM()

        #전처리할 텍스트 연관어 추출
            #명사 추출 함수를 이용
            #사용자 사전에 명사데이터를 추가하면 추출할 단어를 설정가능.
            #ex) 예쁜 NNP --> 명사로 인식해서 추출해온다.
        review_text = raw_data['text']
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        review_text = [hangul.sub('',str(review)) for review in review_text]
        review_text = [review.strip() for review in review_text]
        review_text = [komo.nouns(review_text[i]) for i in range(start, end) if review_text[i] != '']
        
        index = start
        if remove_stopwords:
            # 불용어 제거(선택적)
            for review in review_text:
                word_review = [
                    token for token in review if not token in stop_words]
                word_review = ' '.join(word_review)
                
                if word_review != '':
                    result.append([self.keyword,word_review,raw_data['date'].ix[index]])

                index+=1
        return

    ##전처리 데이터 파일 저장
    def save_data(self,result):
        self.logger.debug("Save data")

        if(self.media == self.MEDIA_MUSINSA):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_MUSINSA
        elif(self.media == self.MEDIA_INSTAGRAM):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_INSTAGRAM

        with open(filepath,'a',encoding="utf-8",newline='') as f:
            wr = csv.writer(f)
            for data in result:
                wr.writerow(data)

        df = pandas.read_csv(filepath,encoding='utf-8',index_col=False)
        df.drop_duplicates().to_csv(filepath,index=False,encoding='utf-8')

    ##전처리된 연관어 데이터에서 연관어 빈도수 추출 함수
    def associate_word_frequency(self,year):
        if(self.media == self.MEDIA_MUSINSA):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_MUSINSA
        elif(self.media == self.MEDIA_INSTAGRAM):
            filepath = self.folder_filepath + self.associate_filename % self.MEDIA_INSTAGRAM
        
        ##날짜 패턴 설정
        pattern = self.date_pattern % (year)
        
        ##말짜 패턴에 매칭되는 값으로 필터링
        df = pandas.read_csv(filepath,index_col=False,encoding='utf-8')
        df = df[df['keyword'] == self.keyword]
        df = df.dropna(how="any")
        df = df.ix[df['date'].str.startswith(pattern),:]
        
        ##연관어 빈도수 사전
        freq_dic = {}
        for words in df['words']:
            for word in words.split():
                ##연관어 추출이니 키워드 자체는 필요x
                if word == self.keyword:
                    continue    

                if word in freq_dic :
                    freq_dic[word] += 1
                else:
                    freq_dic[word] = 1
                    
        freq_items = list(freq_dic.items())
        freq_items.sort(key=lambda item: item[1],reverse=True)
        
        return(freq_items)

if __name__ == '__main__':
    analysis = AssocitatedAnalysis()
    analysis.set_keyword("청바지")
    analysis.set_media(analysis.MEDIA_MUSINSA)

    ##연관어 전처리 과정 
    start_time = time.time()
    analysis.excute_preprocessing() 
    print("time : ", (time.time()-start_time))

    ##연관어 빈도수 리스트 반환 [('연관어',빈도수),.....]
        ##연도를 인자로 넣어줘야 함
    freq = analysis.associate_word_frequency("2019")
    print(freq)
