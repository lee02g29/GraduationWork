from django.forms import ModelForm
from polls.models import *

class PostForm(ModelForm):
    class Meta:
        model = Musinsa
        fields = ['keyword']