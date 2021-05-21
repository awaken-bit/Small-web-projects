from django.shortcuts import render, redirect
from main.models import *
import datetime
from django.db.models import *


# Search
def search_friends(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if request.POST['name']:
                profiles_first_name_list = Profile.objects.filter(owner__first_name__icontains=request.POST['name'])
                profiles_last_name_list = Profile.objects.filter(owner__last_name__icontains=request.POST['name'])
                friends = Profile.objects.get(owner=request.user).friends.all()
                results = set(list(profiles_first_name_list) + list(profiles_last_name_list))
                data = {
                    'profiles': results,
                    'friends': friends,
                }
                return render(request, 'search_and_news/search_friends.html', data)
            else:
                return redirect('search_friends')
        else:
            return render(request, 'search_and_news/search_friends.html')
    else:
        return redirect('login')

def search_groups(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if request.POST['name']:
                groups = Group.objects.filter(name__icontains=request.POST['name'])
                user_groups = Profile.objects.get(owner=request.user).groups.all()
                data = {
                    'groups': groups,
                    'user_groups': user_groups
                }
                return render(request, 'search_and_news/search_groups.html', data)
            else:
                return redirect('search_groups')
        else:
            return render(request, 'search_and_news/search_groups.html')
    else:
        return redirect('login')

# News
def news_list(request):
    if request.method == 'POST':
        pass
    user = request.user
    if user.is_authenticated:
        user = Profile.objects.get(owner=request.user)
        posts = Post.objects.order_by('-id').filter(owner__in=user.friends.all())[:4]
        estimations = []
        for i in posts:
            
            post_estimation = {
                'like': None,
                'dizlike': None
            }
            try:
                Like.objects.get(owner=user, post=i)
                post_estimation['like'] = True
            except:
                pass
            if post_estimation['like'] == True:
                estimations.append(post_estimation)
                continue
            try:
                Dizlike.objects.get(owner=user, post=i)
                post_estimation['dizlike'] = True
            except:
                pass
            estimations.append(post_estimation)
        data = {
            'posts': zip(posts, estimations),
            'ex': estimations
        }
        return render(request, 'search_and_news/news_list.html', data)
    else:
        return redirect('login')

def popular_news_list(request):
    if request.method == 'POST':
        pass
    user = request.user
    if user.is_authenticated:
        user = Profile.objects.get(owner=request.user)
        posts = Post.objects.annotate(rating=Count('comment') + Count('like') + Count('dizlike')).order_by('-rating')[:4]
        """ posts = list(posts)
        posts.sort(key=lambda x: x.comment__count)
        posts = posts[::-1] """
        estimations = []
        for i in posts:
            
            post_estimation = {
                'like': None,
                'dizlike': None
            }
            try:
                Like.objects.get(owner=user, post=i)
                post_estimation['like'] = True
            except:
                pass
            if post_estimation['like'] == True:
                estimations.append(post_estimation)
                continue
            try:
                Dizlike.objects.get(owner=user, post=i)
                post_estimation['dizlike'] = True
            except:
                pass
            estimations.append(post_estimation)
        data = {
            'posts': zip(posts, estimations),
            'ex': estimations
        }
        return render(request, 'search_and_news/popular_news_list.html', data)
    else:
        return redirect('login')

def create_post(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            speks = request.POST
            profile = Profile.objects.get(owner=user)
            if 'file_post' in speks:
                post = Post(
                    owner=profile,
                    text=speks['text_post'],
                    pub_date=datetime.datetime.today(),
                )
                post.save()
            else:
                post = Post(
                    owner=profile,
                    text=speks['text_post'],
                    pub_date=datetime.datetime.today(),
                    image=request.FILES['file_post']
                )
                post.save()

        return redirect('home', user.id)
    else:
        return redirect('login')