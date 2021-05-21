from main.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from django.db.models import *

import datetime


class LikeOrDizlikeView(APIView):
    def get(self, request):
        return Response({"message": 'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(owner=user)
            speks = request.data
            
            try:
                id = int(speks['id'])
            except:
                return Response({"message": 'Id должен быть числом'})

            try:
                post = Post.objects.get(id=id)
            except:
                return Response({"message": 'Нет такой записи'})

            if 'like' in  speks:
                if post.like_set.filter(post=post).count() == 0 and post.dizlike_set.filter(post=post).count() == 0:
                    obj = Like(owner=profile, post=post)
                    obj.save()
                    return Response({"message": 'Лайк'})
                else:
                    return Response({"message": 'Вы уже оценивали этот пост'})
            elif 'dizlike' in speks:
                if post.dizlike_set.filter(post=post).count() == 0 and post.like_set.filter(post=post).count() == 0:
                    obj = Dizlike(owner=profile, post=post)
                    obj.save()
                    return Response({"message": 'Дизлайк'})
                else:
                    return Response({"message": 'Вы уже оценивали этот пост'})
            else:
                return Response({"message": 'Ошибка в данных'})
        else:
            return Response({"message": 'Вы не зарегистрированны'})

class CommentView(APIView):
    def get(self, request):
        return Response({"message": 'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(owner=user)
            speks = request.data
            try:
                id = int(speks['id'])
            except:
                return Response({"message": 'Некорректный id'})
            
            try:
                post = Post.objects.get(id=id)
            except:
                return Response({"message": 'Нет такого поста'})
            
            comments = Comment.objects.filter(post=post)
            
                
            if 'text' in speks:
                comment = Comment(
                    owner=profile,
                    post=post,
                    text=speks['text'],
                    date=datetime.datetime.today()
                )
                comment.save()
                return Response({"message": 'Success', "data":serializers.CommentSerializer(comment).data})
            else:
                
                
                serializer = serializers.CommentSerializer(comments, many=True)
                return Response({"message":{'comments': serializer.data}})
        else:
            return Response({"message": 'Вы не зарегистрированны'})

class DynamicPostLoad(APIView):
    def get(self, request):
        return Response({"message": 'Тут ничего нет :)'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(owner=user)
            speks = request.data
            if 'user' in speks:
                posts = Post.objects.order_by('-id').filter(id__lt=int(speks['last_post']), owner=profile)[:4]
            else:
                if 'popular_posts' in speks:
                    try:
                        last_post = Post.objects.get(id=int(speks['last_post']))
                    except:
                        return Response({"message": 'Нет такого поста'})
                    last_post_rating = last_post.comment_set.count() + last_post.like_set.count() + last_post.dizlike_set.count()
                    posts = Post.objects.annotate(rating=Count('comment') + Count('like') + Count('dizlike')).order_by('-rating').filter(rating__lt=last_post_rating)[:4]
                else:
                    posts = Post.objects.order_by('-id').filter(id__lt=int(speks['last_post']), owner__in=profile.friends.all())[:4]
            data = []
            
            for i in posts:
                obj = {
                    'id':i.id,
                    'image': i.image.url if i.image else None,
                    'profile': f"{i.owner.owner.first_name} {i.owner.owner.last_name}",
                    'text': i.text,
                    'pub_date': f"{i.pub_date.day}-{i.pub_date.month}-{i.pub_date.year} {i.pub_date.hour}:{i.pub_date.minute}",
                    'likes':{
                        'count': i.like_set.count(),
                        'my': True if {'owner':profile.id} in i.like_set.values('owner') else None
                    },
                    'dizlikes': {
                        'count': i.dizlike_set.count(),
                        'my': True if {'owner':profile.id} in i.dizlike_set.values('owner') else None
                    },
                    'comments': i.comment_set.count()
                }
                data.append(obj)
            if len(data) != 0:
                
                data[-1]['last_post'] = True
                
            return Response({"message": data})
        else:
            return Response({"message": 'Вы не зарегистрированны'})
