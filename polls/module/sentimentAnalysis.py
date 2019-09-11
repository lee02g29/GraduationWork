import pandas
import csv
import pickle
import numpy
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class SentimentAnalysis():
    def __init__(self):
        self.filepath = "polls/module/data/"
        self.modelFile = "tf_idf_model.pkl"
        self.preproFile = None
        self.model = None
        self.keyword = None
        self.media = None
        self.MEDIA_MUSINSA = "musinsa"
        self.MEDIA_INSTAGRAM = "instagram"
        self.CATEGORY = ['color','price','size','None']
        self.months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        self.yearlist = []

        self.load_model()

    ##키워드설정
    def set_keyword(self,keyword):
        self.keyword = keyword

    def get_keyword(self):
        return self.keyword
    
    ##매체설정
    def set_media(self,media):
        self.media = media

        ##전처리 파일 선택
        if self.media == self.MEDIA_INSTAGRAM:
            self.preproFile = "preprocessed_instagram.csv"
            self.date_pattern = "%s-%s-"
        elif self.media == self.MEDIA_MUSINSA:
            self.preproFile = "preprocessed_musinsa.csv"
            self.date_pattern = "%s.%s."
    
    def get_media(self):
        return self.media

    ##현재 저장되어있는 리뷰 연도리스트 반환
    def get_year_list(self):
        filepath = self.filepath+self.preproFile
        now = time.localtime() ##현재날짜

        for year in range(now.tm_year,now.tm_year-3,-1): ##현재 연도로부터 3년간 데이터 존재하는지 
            df = pandas.read_csv(filepath,encoding='utf-8',index_col=False)
            df = df[df['keyword'] == self.keyword]
            df = df.dropna(how="any")
            pattern = str(year)
            df = df.ix[df['date'].str.startswith(pattern),:]
            if(len(df) != 0):
                self.yearlist.append(year)
        return self.yearlist    

    ##감정분석 학습 모델 로드
    def load_model(self):
        with open(self.filepath+self.modelFile,'rb') as f:
            self.model = pickle.load(f)

    ##긍/부정 예측
    def predict_sentiment_month(self,year,month,detailed="no"):
        month = str(month)
        if len(month) == 1: 
            month = "0"+month
        if month not in self.months : raise Exception
        
        ##날짜 패턴 설정
        pattern = self.date_pattern % (year,month)

        ##전처리 데이터 불러오고 필터링
        data = pandas.read_csv(self.filepath+self.preproFile,encoding='utf-8',index_col=False)
        data = data[data['keyword']==self.keyword]
        if detailed != "no":
            data = data[data['category']==detailed]
        data = data.dropna(how="any")
        data = data.ix[data['date'].str.startswith(pattern),:]
        review_data = [str(review) for review in data['text']]

        result = {"pos":0, "neg":0}

        ##예외처리
        if len(review_data) == 0:
            return result

        ##긍/부정 예측
        pred = self.model.predict(review_data)
        ##probability = numpy.max(self.model.predict_proba(example))*100
        
        ##긍/부정 카운트 
        for sentiment in pred:
            if sentiment == 1:
                result["pos"] = result["pos"] + 1
            elif sentiment == -1:
                result["neg"] = result["neg"] + 1

        return result
    
if __name__ == '__main__':
    analysis = SentimentAnalysis()
    analysis.set_keyword('맨투맨')
    analysis.set_media(analysis.MEDIA_MUSINSA)
    for month in analysis.months:
        l = analysis.predict_sentiment_month("2018",month)
        print("%2s - %s" % (month,l))
    print() 
