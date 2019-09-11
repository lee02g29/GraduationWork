from django.contrib import admin
from .models import Instagram, Musinsa, Musinsa_Mention, Instagram_Mention, Musinsa_association, Instagram_association, Musinsa_sentiment, Instagram_sentiment

admin.site.register(Instagram)
admin.site.register(Musinsa)
admin.site.register(Musinsa_Mention)
admin.site.register(Instagram_Mention)
admin.site.register(Musinsa_association)
admin.site.register(Instagram_association)
admin.site.register(Musinsa_sentiment)
admin.site.register(Instagram_sentiment)