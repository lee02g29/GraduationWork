from django.db import models

# Create your models here.
##뷰에 가공할 데이터를 조작하는 부분
    ##모델은 기본적으로 class로 생성
    ##Filed를 이용해 가져오는 것. -> 다양한 Filed 존재 찾아볼 것

class Instagram(models.Model):
    keyword = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    dates = models.DateTimeField('dates')

    def __str__(self):
        return self.keyword

class Musinsa(models.Model):
    keyword = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    dates = models.DateTimeField('dates')
    rank = models.BigIntegerField()

    def __str__(self):
        return self.keyword

##언급량 
class Musinsa_Mention(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    mentions = models.BigIntegerField()  
    reviews = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year + '.' + self.month

class Instagram_Mention(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    mentions = models.BigIntegerField()
    reviews = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year + '.' + self.month

##연관어
class Musinsa_association(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    association = models.CharField(max_length=200)
    frequency = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year

class Instagram_association(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    association = models.CharField(max_length=200)
    frequency = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year

##긍/부정
class Musinsa_sentiment(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    category = models.CharField(max_length=200)
    pos = models.BigIntegerField()
    neg = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year + '.' + self.month

class Instagram_sentiment(models.Model):
    keyword = models.CharField(max_length=200, default='DEFAULT VALUE')
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    category = models.CharField(max_length=200)
    pos = models.BigIntegerField()
    neg = models.BigIntegerField()

    def __str__(self):
        return self.keyword + ',' + self.year + '.' + self.month
