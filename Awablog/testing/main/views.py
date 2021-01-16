from django.shortcuts import render, redirect
from .models import Author, Blog, Entry, Likeq, User_vie, Dizlikeq

from django.views.generic import DetailView
import datetime

def delete_post(request, pk):
    autors = [ i.author_blog.all() for i in Entry.objects.get(id=pk).blog.all()]
    #autors = [i.user_main.all() for i in autors]
    #autors = [i.id for i in autors]
    autors = [ i.user_main.all() for i in autors[0]][0]
    autors = [ i.id for i in autors]
    print(autors[0])
    if request.user.id == autors[0]:
        blog_id = Entry.objects.get(id=pk).blog.all()
        for i in blog_id:
            s = i.id

        del_entr = Blog.objects.get(id=s).entry_set.all()

        for i in del_entr:
            del_entr = i 
        del_entr.delete()

        return redirect('blog_post', s)
    else:
        return render(request, 'account/messeng.html',{'mes': '<p>Вы не автор этой статьи</p>'})

def blogsposts(request, pk):
    blog = Blog.objects.get(id=pk)
    return render(request, 'main/blog_post.html', {'note': blog})

def create_post(request, pk):
    if request.method == 'POST':
        print(request.POST['headline'])
        print(request.POST['body_text'])
        today = datetime.datetime.today()
        entr = Entry(
            headline= request.POST['headline'],
            body_text= request.POST['body_text'],
            pub_date= today.strftime("%Y-%m-%d"),
        )
        entr.save()
        entr.authors.add(Author.objects.get(user_main__id=request.user.id))
        entr.blog.add(Blog.objects.get(author_blog__user_main__id=request.user.id))

        return redirect('blog_post',pk)
    else:
        try:
            blogd = Blog.objects.get(author_blog__user_main__id=request.user.id)
        except:
            return render(request,'account/messeng.html',{'mes': '<p>Вы не автор этой статьи</p>'})
        return render(request, 'main/create_post.html',{'pk': pk})


class BlogPost(DetailView):
    model = Entry
    template_name = 'main/post.html'
    context_object_name = 'note'

def dashboard(request):
    if request.method == 'POST':
        if request.POST['1'] == '1':
            author = Author()
            author.save()
            author.user_main.add(request.user)
            return redirect('create_blog')
        else:
            user_vie = User_vie()
            user_vie.save()
            user_vie.user_main.add(request.user)
            return redirect('home')
    else:
        try:
            my_blog = Blog.objects.get(author_blog__user_main__id=request.user.id).id
        except:
            my_blog = ''
        new_user = True
        if Blog.objects.filter(author_blog__user_main__id=request.user.id).count() >= 1 or User_vie.objects.filter(user_main__id=request.user.id).count() >= 1:
            new_user = False
        return render(request, 'account/dashboard.html', {
            'data_id': my_blog,
            'new_user': new_user
            })


def create_blog(request):
    if request.method == 'POST':
        blog = Blog(name=request.POST['blog'], tagline=request.POST['tagline'])
        blog.save()
        blog.author_blog.add(Author.objects.get(user_main__id=request.user.id))
        return redirect('home')
    else:
        new_user = True
        if Blog.objects.filter(author_blog__user_main__id=request.user.id).count() >= 1 or User_vie.objects.filter(user_main__id=request.user.id).count() >= 1:
            new_user = False
        return render(request, 'main/create_blog.html', {'new_user': new_user})



def index(reqest):
    dd = list(Dizlikeq.objects.filter(post__headline='HTML'))
    sd = [ i for i in list(Likeq.objects.filter(post__headline='Обо мне'))]
    b = list(Likeq.objects.filter(post__headline='HTML'))
    data = {
        'test': sd,
        'blog': Blog.objects.order_by('-id'),
        'author': Author.objects.order_by('id'),
        'entry': Entry.objects.order_by('-id'),
        'entry_data': {
            'blog':[i.blog.all() for i in Entry.objects.order_by('-id')],
            'body_text':[ i.body_text for i in Entry.objects.order_by('-id')],
            'authors':[i.authors.all()[0] for i in Entry.objects.order_by('-id')],
            'headline': [i.headline for i in Entry.objects.order_by('-id')],
        }
    }
    note = []
    a = 0
    for i in data['entry_data']['headline']:
        note.append({'headline': i})
        a += 1
    a = 0
    for i in data['entry_data']['authors']:
        note[a]['author'] = i
        a += 1
    a = 0
    for i in data['entry_data']['body_text']:
        note[a]['body_text'] = i
        a += 1
    a = 0
    for i in data['entry_data']['blog']:
        note[a]['blog'] = i[0]
        a += 1
    a = 0



    data['note'] = note
    return render(reqest, 'main/main.html', data)





def blogs_home(reqest):
    data = {
        'blogs': Blog.objects.order_by('-id'),
    }
    return render(reqest, 'main/blogs.html',data)

def like(reqest, pk):
    if Likeq.objects.filter(author=reqest.user,post=Entry.objects.get(id=pk)).count() >= 1:
        return render(reqest,'account/messeng.html',{'mes': '<p>Вы уже оценивали этот пост</p>'})
    else:
        post_i = Entry.objects.get(id=pk)
        author_i = reqest.user

        #post_i.likeq_set.create(author=author_i)
        s = Likeq()
        s.save()
        s.author.add(author_i)
        s.post.add(post_i)
        #s = Likeq.objects.create(post=post_i, author=author_i)
        #s.save()

        return redirect('post_us',pk)


def dizlike(reqest, pk):
    if Dizlikeq.objects.filter(author=reqest.user,post=Entry.objects.get(id=pk)).count() >= 1:
        return render(reqest,'account/messeng.html',{'mes': '<p>Вы уже оценивали этот пост</p>'})
    else:
        post_i = Entry.objects.get(id=pk)
        author_i = reqest.user

        #post_i.likeq_set.create(author=author_i)
        s = Dizlikeq()
        s.save()
        s.author.add(author_i)
        s.post.add(post_i)
        #s = Likeq.objects.create(post=post_i, author=author_i)
        #s.save()

        return redirect('post_us',pk)
























"""
    for i in note:
        com_lis = [ i.like for i in list(Comment.objects.filter(post__headline=i['headline']))]
        like = 0
        dizlike = 0
        for h in com_lis:
            if h == -1:
                dizlike += 1
            else:
                like += 1
        i['like'] = like
        i['dizlike'] = dizlike
"""