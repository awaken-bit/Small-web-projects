from django.shortcuts import redirect, render
from .models import * 

from django.core.cache import cache


def index(request, pk):
    try:
        profile = Profile.objects.get(owner__id=pk)
        data = {
                    'profile':profile,
                    'posts': profile.post_set.order_by('-id').all()[:4],
                }
        return render(request, 'main/main.html', data)
        
    except:
        return render(request, 'account/messeng.html', {'mes': '<h1>Нет такого пользователя</h1>'})

def home(request):
    post = Post.objects.get(id=5)

    data = {
        'post': post.owner_id
    }
    return render(request, 'main/home.html', data)

# Chats
def chat(request, pk):
    senders = Messange.objects.filter(sender__owner__id=pk, addressee__owner__id=request.user.id)
    addresseens = Messange.objects.filter(addressee__owner__id=pk, sender__owner__id=request.user.id)
    messanges = list(senders) + list(addresseens)
    messanges.sort(key=lambda x: x.id)
    data = {
        'messanges': messanges,
        'adressen':pk,
        
    }
    return render(request, 'main/chat.html', data)

def chat_group(request, pk):
    try:
        sistem_user = Profile.objects.get(owner__id=request.user.id)
    except:
        return render(request, 'account/messeng.html', {'mes': '<h1>Вы не зарегистрированны</h1>'})
    group = Group.objects.get(id=pk)
    if sistem_user in group.participants.all() or group.admin == sistem_user:
        messanges = group.messangegroup_set.all()
        data = {
            'messanges': messanges,
            'group': group,
            'profile': sistem_user
        }
        return render(request, 'main/chat_group.html', data)
    else:
        return render(request, 'account/messeng.html', {'mes': '<h1>Вы не участник этой группы</h1>'})

# Friends
def delete_friend(request, pk):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner=user)
        delete_friend = Profile.objects.get(owner__id=pk)
        profile.friends.remove(delete_friend)
        
        return redirect('friends_list')
    else:
        return redirect('login')

def append_friend(request, pk):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner=user)
        delete_friend = Profile.objects.get(owner__id=pk)
        profile.friends.add(delete_friend)
        
        return redirect('friends_list')
    else:
        return redirect('login')

def friends_list(request):
    user = request.user
    if user.is_authenticated:
        data = {
            'friends': Profile.objects.get(owner=request.user).friends
        }
        return render(request, 'main/friends.html', data)
    else:
        return redirect('login')

def messanges_friends_list(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner__id=request.user.id)
        new_messanges = []
        messange_profiles = []
        for i in profile.adress.order_by('-id'):
            if i.sender not in messange_profiles:
                new_messanges.append(i.text)
                messange_profiles.append(i.sender)

        messanges_friends_list = zip(new_messanges, messange_profiles)

        data = {
            'messanges_friends_list': messanges_friends_list,
        }
        return render(request, 'main/messanges_list.html', data)
    else:
        return redirect('login')

# Groups
def create_group(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(owner=user)
            
            group_text = request.POST['group_text']
            group_name = request.POST['group_name']
            if 'group_img' in request.FILES:
                group_img = request.FILES['group_img']
                extensions = ['png', 'jpg', 'jpeg']
                if group_img.name.split('.')[1] in extensions:
                    group = Group(
                        admin=profile,
                        text=group_text,
                        name=group_name,
                        image=group_img
                    )
                    group.save()
                    group.participants.add(profile)
                    profile.groups.add(group)
                else:
                    return render(request, 'account/messeng.html', {'mes': '<h1>Некорректное расширение файла</h1>'})
            else:
                group = Group(
                    admin=profile,
                    text=group_text,
                    name=group_name
                )
                group.save()
            return redirect('groups_list')
        else:
            return redirect('login')
    else:
        return render(request, 'main/create_group.html')

def delete_group(request, pk):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner=user)
        
        delete_group = Group.objects.get(id=pk)
        profile.groups.remove(delete_group)
        
        return redirect('groups_list')
    else:
        return redirect('login')

def append_group(request, pk):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner=user)
        
        delete_group = Group.objects.get(id=pk)
        profile.groups.add(delete_group)
        
        return redirect('groups_list')
    else:
        return redirect('login')

def group_settings(request, pk):
    user = request.user
    if user.is_authenticated:
        try:
            group = Group.objects.get(id=pk)
        except:
            return render(request, 'account/messeng.html', {'mes': '<h1>Нет такой группы</h1>'})
        
        profile = Profile.objects.get(owner=user)
        
        if request.method == 'POST':
            if group.admin == profile:
                speks = dict(request.POST)
                print(speks)
                if 'appended_participants' in speks:
                    try:
                        list_id = map(lambda x: int(x), speks['appended_participants'])
                    except:
                        return render(request, 'account/messeng.html', {'mes': '<h1>Некорректные данные</h1>'})
                    for i in list_id:
                        group.participants.add(Profile.objects.get(id=i))
                elif 'deleted_participants' in speks:
                    try:
                        list_id = map(lambda x: int(x), speks['deleted_participants'])
                    except:
                        return render(request, 'account/messeng.html', {'mes': '<h1>Некорректные данные</h1>'})
                    for i in list_id:
                        group.participants.remove(Profile.objects.get(id=i))
                elif 'group_text' in speks:
                    speks =  request.POST
                    if speks['group_text'] != group.text:
                        group.text = speks['group_text']
                        group.save()
                    if speks['group_name'] != group.name:
                        group.name = speks['group_name']
                        group.save()
                    if 'group_img' in request.FILES:
                        file = request.FILES['group_img']
                        extensions = ['png', 'jpg', 'jpeg']
                        if file.name.split('.')[1] in extensions:
                            group.image = file
                            group.save()
                
                return redirect('settings_group', group.id)
            else:
                return render(request, 'account/messeng.html', {'mes': '<h1>Вы не админ этой группы</h1>'})
        else:
            
            if group.admin == profile:
                data = {
                    'group':group,
                    'profile':profile
                }
                return render(request, 'main/settings_group.html', data)
            else:
                return render(request, 'account/messeng.html', {'mes': '<h1>Вы не админ этой группы</h1>'})
    else:
        return redirect('login')

def messanges_groups_list(request):
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(owner=request.user)
        groups = profile.groups.all()
        groups_messanges = []
        for i in groups:
            try:
                groups_messanges.append(MessangeGroup.objects.order_by('-id').get(addressee_group=i).text)
            except:
                groups_messanges.append('Пока сообщений нет')
        data = {
            'groups_list': zip(groups, groups_messanges),
            'profile':profile
        }
        return render(request, 'main/messanges_groups_list.html', data)
    else:
        return redirect('login')