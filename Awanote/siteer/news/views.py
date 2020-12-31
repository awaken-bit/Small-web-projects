from django.shortcuts import render, redirect
from  .models import Artiles
from .forms import ArtilesForm
from django.views.generic import DetailView, UpdateView, DeleteView


class NewsDeleteAR(DeleteView):
    model = Artiles
    template_name = 'news/delete.html'
    success_url = '/news/'


class NewsUpdateAR(UpdateView):
    model = Artiles
    template_name = 'news/update.html'
    form_class = ArtilesForm

# Create your views here.
def news_home(reqest):
    news = Artiles.objects.order_by('-id')
    return render(reqest, 'news/news_home.html', {'news': news})

def create(reqest):
    error = ''
    if reqest.method == 'POST':
        form = ArtilesForm(reqest.POST)
        if form.is_valid():
            form.save()
            return redirect('news_home')
        else:
            error = 'Форма неправильно заполнена'
    form = ArtilesForm()


    data = {
        
        'form': form,
        'error': error
    }
    return render(reqest, 'news/create.html', data)