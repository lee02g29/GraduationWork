from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from .models import Musinsa_Mention, Instagram_Mention, Musinsa_association, Instagram_association, Musinsa_sentiment, Instagram_sentiment
from .module.Crawler.crawler_client import *
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect    
from django.shortcuts import redirect

from .module.Preprocessing import *
from .module.associatedAnalysis import *
from .module.DataAnalysis import *
from .module.sentimentAnalysis import *

MEDIA_MUSINSA = "musinsa"
MEIDA_INSTAGRAM = "instagram"

##사용자에게 보여주는 작업
    ##html 랜더링
    ##데이터베이스 접근 등 - 구체적인 일은 model이용
@csrf_exempt
def index(request):
    print(request.method)

    ##POST요청 처리
    if request.method == "POST":
        ##키워드,매체 설정
        keyword = request.POST.get('keyword')
        media = request.POST.get('media')

        if(media == "undefined" or keyword == "undefined"):
            return HttpResponse('Hello world')

        print("receive POST - %s, %s" % (keyword,media))

        ##전처리과정 
        prepro = Preprocessor()
        prepro.set_keyword(keyword)
        prepro.set_media(media)
        isZero = prepro.excute_preprocessing()

        if(isZero == "zeroData"):
            return HttpResponse('Hello world')

        ##언급량분석
        analysis = MentionAnalysis()
        analysis.set_Keyword(keyword)  
        analysis.set_Media(media) 

        years = analysis.get_year_list() ##연도 리스트
        for year in years:
            analysis.set_Year(str(year)) ##연도 설정    
            mentions = analysis.get_mention_for_year() ##설정한 연도에 해당하는 월별 언급량 리스트 
            for mention in mentions:
                if(media == MEDIA_MUSINSA):
                    obj = Musinsa_Mention.objects.filter(keyword=keyword,year=year,month=mention[0]) ##DB 검색
                else:
                    obj = Instagram_Mention.objects.filter(keyword=keyword,year=year,month=mention[0])

                if list(obj) != []:  ##이미 데이터 존재하면
                    obj.update(mentions=mention[1],reviews = mention[2]) ##업데이트
                else:
                    ##데이터 없으면 삽입
                    if(media == MEDIA_MUSINSA):
                        Musinsa_Mention(keyword=keyword, year=year, month=mention[0], mentions = mention[1], reviews = mention[2]).save()
                    else:
                        Instagram_Mention(keyword=keyword, year=year, month=mention[0], mentions = mention[1], reviews = mention[2]).save()

            print("%s MentionAnalysis Success"%(year))
        print("Successfully MentionAnalysis and saved")



        ##연관어분석
        analysis = AssocitatedAnalysis()
        analysis.set_keyword(keyword)
        analysis.set_media(media)
        analysis.excute_preprocessing() ##연관어 전처리
        
        years = analysis.get_year_list()
        for year in years:
            freqs = analysis.associate_word_frequency(year)
            for freq in freqs:
                if media == MEDIA_MUSINSA:
                    obj = Musinsa_association.objects.filter(keyword=keyword, year=year, association=freq[0])
                else:
                    obj = Instagram_association.objects.filter(keyword=keyword, year=year, association=freq[0])

                if list(obj) != []:
                    obj.update(frequency=freq[1])
                else:
                    if media == MEDIA_MUSINSA:    
                        Musinsa_association(keyword=keyword, year=year, association=freq[0], frequency=freq[1]).save()
                    else:
                        Instagram_association(keyword=keyword, year=year, association=freq[0], frequency=freq[1]).save()

            print("%s AssocitatedAnalysis Success"%(year))
        print("Successfully AssocitatedAnalysis and saved")

        ##긍/부정분석
        analysis = SentimentAnalysis()
        analysis.set_keyword(keyword)
        analysis.set_media(media)
        years = analysis.get_year_list()
        for year in years:
            for month in analysis.months:
                result = analysis.predict_sentiment_month(year,month)
                if media == MEDIA_MUSINSA:
                    obj = Musinsa_sentiment.objects.filter(keyword=keyword, year=year, month=month)
                else:
                    obj = Instagram_sentiment.objects.filter(keyword=keyword, year=year, month=month)

                if list(obj) != []:
                    obj.update(category="no",pos=result['pos'], neg=result['neg'])
                else:
                    if media == MEDIA_MUSINSA:
                        Musinsa_sentiment(keyword=keyword, year=year, month=month, category="no",pos=result['pos'], neg=result['neg']).save()
                    else:
                        Instagram_sentiment(keyword=keyword, year=year, month=month, category="no",pos=result['pos'], neg=result['neg']).save()

            print("%s SentimentAnalysis Success"%(year))
        print("Successfully SentimentAnalysis and saved")

        ##긍/부정 - 세부분석
        for year in years:
            for month in analysis.months:
                for category in analysis.CATEGORY:
                    result = analysis.predict_sentiment_month(year,month,category)
                    if media == MEDIA_MUSINSA:
                        obj = Musinsa_sentiment.objects.filter(keyword=keyword, year=year, month=month,category=category)
                    else:
                        obj = Instagram_sentiment.objects.filter(keyword=keyword, year=year, month=month,category=category)
            
                    if list(obj) != []:
                        obj.update(category=category,pos=result['pos'], neg=result['neg'])
                    else:
                        if(media == MEDIA_MUSINSA):
                            Musinsa_sentiment(keyword=keyword, year=year, month=month, category=category,pos=result['pos'], neg=result['neg']).save()
                        else:
                            Instagram_sentiment(keyword=keyword, year=year, month=month, category=category,pos=result['pos'], neg=result['neg']).save()
                            
                    print("%s SentimentAnalysis-detailed Success"%(category))
            print("%s SentimentAnalysis-detailed Success"%(year))
        print("Successfully SentimentAnalysis-detailed and saved")

        template = loader.get_template('polls/index.html')
        request.encoding = 'utf-8'

        musinsamen = Musinsa_Mention.objects.values()
        instagrammen = Instagram_Mention.objects.values()
        musinsa_mention = [data for data in musinsamen]
        instagram_mention = [data for data in instagrammen]

        musinsa_ass = Musinsa_association.objects.values()
        instagram_ass = Instagram_association.objects.values()
        musinsa_association = [data for data in musinsa_ass]
        instagram_association = [data for data in instagram_ass]

        musinsa_sent = Musinsa_sentiment.objects.values()
        instagram_sent = Instagram_sentiment.objects.values()
        musinsa_sentiment = [data for data in musinsa_sent]
        instagram_sentiment = [data for data in instagram_sent]

        context = {'musinsa_mention': musinsa_mention, 'instagram_mention': instagram_mention, 'musinsa_association': musinsa_association, 'instagram_association': instagram_association,
                'musinsa_sentiment':musinsa_sentiment, 'instagram_sentiment' : instagram_sentiment, 'keyword': keyword}
        
        return HttpResponse(template.render(context, request))
    ##GET 요청처리
    else:
        keyword = request.GET.get('keyword')
        # media = request..get('media')
        print(keyword)

        template = loader.get_template('polls/index.html')
        request.encoding = 'utf-8'

        musinsamen = Musinsa_Mention.objects.values()
        instagrammen = Instagram_Mention.objects.values()
        musinsa_mention = [data for data in musinsamen]
        instagram_mention = [data for data in instagrammen]

        musinsa_ass = Musinsa_association.objects.values()
        instagram_ass = Instagram_association.objects.values()
        musinsa_association = [data for data in musinsa_ass]
        instagram_association = [data for data in instagram_ass]

        musinsa_sent = Musinsa_sentiment.objects.values()
        instagram_sent = Instagram_sentiment.objects.values()
        musinsa_sentiment = [data for data in musinsa_sent]
        instagram_sentiment = [data for data in instagram_sent]

        context = {'musinsa_mention': musinsa_mention, 'instagram_mention': instagram_mention, 'musinsa_association': musinsa_association, 'instagram_association': instagram_association,
                'musinsa_sentiment':musinsa_sentiment, 'instagram_sentiment' : instagram_sentiment, 'keyword': keyword}
        
        return HttpResponse(template.render(context, request))
        
       


# Create your views here.
def error(request):
    template = loader.get_template('polls/404.html')
    context= {}
    return HttpResponse(template.render(context, request))