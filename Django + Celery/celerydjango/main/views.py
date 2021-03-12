from django.shortcuts import render
from .models import News, Politicon
# Create your views here.
def index(reqest):
    all_news = News.objects.all()
    cours = Politicon.objects.all()[0]
    
    return render(reqest, 'main.html', {
        'news': all_news,
        'cours': cours
    })

def new_content(reqest, pk):
    try:
        content = News.objects.get(id=pk)
    except:
        return render(reqest, 'messeng.html', {
        'mes': 'Нет такой записи.'
    })
    return render(reqest, 'content_new.html', {
        'content': content
    })