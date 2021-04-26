from django.shortcuts import render, redirect
from  .models import Artiles
from .forms import ArtilesForm

def delete_news(request, pk):
    note = Artiles.objects.get(id=pk)
    if note.who == request.user.id:
        note.delete()
        return redirect('news_home')
    else:
        return redirect('news_home')


def news_home(reqest):
    news = Artiles.objects.order_by('-id')
    error = ''
    if reqest.method == 'POST':
        if 'news_text' in reqest.POST:
            note = Artiles.objects.get(id=reqest.POST['news_id'])
            if note.who == reqest.user.id:
                note.text = reqest.POST['news_text']
                note.title = reqest.POST['news_title']
                note.save()
            else:
                return redirect('news_home')
        else:
            form = ArtilesForm(reqest.POST)
            if form.is_valid():
                form.save()
                return redirect('news_home')
            else:
                error = 'Форма неправильно заполнена'
    form = ArtilesForm()


    data = {
        
        'form': form,
        'error': error,
        'news': news,
    }
    return render(reqest, 'news/news_home.html', data)
