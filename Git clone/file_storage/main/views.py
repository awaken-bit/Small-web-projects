from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse, Http404
from file_storage.settings import MEDIA_ROOT
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import urllib
import zipfile
import datetime


# Other
def main(request):
    return render(request, 'main/main.html')

def follow(request, slug):
    if request.user.is_authenticated:
        profile = request.user.profile
        try:
            follow_profile = Profile.objects.get(slug=slug)
        except:
            raise Http404
        
        if profile == follow_profile:
            raise Http404
        
        if follow_profile in profile.favorites.all():
            profile.favorites.remove(follow_profile)
        else:
            profile.favorites.add(follow_profile)

        profile.save()
        return redirect('dashboard', follow_profile.slug)
    else:
        raise Http404

def search_repositorys(request):
    if request.method == 'POST':
        speks = request.POST
        repositorys = Repository.objects.select_related('owner') \
        .order_by('-changed_at').filter(name__icontains=speks['name'], is_private=False)[:5]
        answer = []
        for i in repositorys:
            answer.append([
                i,
                timedelta_to_dhms(
                    datetime.datetime.today() - datetime.datetime(
                    i.changed_at.year,
                    i.changed_at.month,
                    i.changed_at.day,
                    i.changed_at.hour, 
                    i.changed_at.minute)
                )
            ])
            
        data = {
            'repositorys': answer,
            'lenght': len(answer),
            'query': speks['name']
        }
        return render(request, 'main/search_repositorys.html', data)
    else:
        return render(request, 'main/search_repositorys.html')
# File
def get_file(request, pk):
    try:
        file = Document.objects.get(id=pk)
        if file.repository.is_private and file.repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    root = str(MEDIA_ROOT).replace('\\', '/') + '/'
    
    path_to_file = f'{root}/{file.file}'

    try:
        finall_file = [open(path_to_file, 'r', encoding='utf-8').read(), 'read']
    except:
        finall_file = [file.file.url, 'not_read']
    data = {
        'file': finall_file,
        'file_data': file,
        'folder_tree': merge_list(folder_tree(file.folder)) if file.folder else None,
        'repository': file.repository,
    }
    return render(request, 'main/file_view.html', data)

def create_file(request):
    if request.method == 'POST' and request.user.is_authenticated:
        speks = request.POST
        file = SimpleUploadedFile(speks['name'], speks['content'].encode('utf-8'))
        
        print(file, file.read().decode('utf-8'))
        if speks['where_to'] == 'repository':
            try:
                repository = Repository.objects.get(id=int(speks.get('id')))
            except:
                raise Http404

            if request.user.profile != repository.owner:
                raise Http404
            
            try:
                repository.document_set.get(name=speks.get('name'))
            except:
                pass
            else:
                data = {
                    'repository': repository,
                    'messeng': 'Файл с таким именем уже существует.'
                }
                return render(request, 'main/repository_settings.html', data)
            
            repository_files = repository.document_set.all()
            new_file = Document(
                repository = repository,
                name = speks.get('name'),
                file = file,
                created_at = datetime.datetime.today(),
                changed_at = datetime.datetime.today()
            )
            try:
                same_file = repository_files.get(name=speks['name'])
            except:
                pass
            else:
                same_file.delete()
            new_file.save()
            return redirect('repository_view', repository.id)
        else:
            try:
                folder = Folder.objects.get(id=int(speks.get('id')))
            except:
                raise Http404

            if request.user.profile != folder.owner.owner:
                raise Http404
            
            try:
                folder.document_set.get(name=speks.get('name'))
            except:
                pass
            else:
                data = {
                    'folder': folder,
                    'messeng': 'Файл с таким именем уже существует.'
                }
                return render(request, 'main/folder_settings.html', data)

            folder_files = folder.document_set.all()
            new_file = Document(
                repository = folder.owner,
                folder = folder,
                name = speks.get('name'),
                file = file,
                created_at = datetime.datetime.today(),
                changed_at = datetime.datetime.today()
            )
            try:
                same_file = folder_files.get(name=speks['name'])
            except:
                pass
            else:
                same_file.delete()
            new_file.save()
            return redirect('folder_view', folder.id)
    else:
        raise Http404

def edit_file(request, pk):
    if request.method == 'POST':
        try:
            file = Document.objects.get(id=pk)
            if file.repository.owner != request.user.profile:
                raise Http404
        except:
            raise Http404
        speks = request.POST
        
        date = datetime.datetime.today()
        
        if speks['filename'] != file.name:
            try:
                if file.folder:
                    file.folder.document_set.get(name=speks['filename'])
                else:
                    file.repository.document_set.get(name=speks['filename'])
            except:
                pass
            else:
                raise Http404('Файл с таким именем уже существует.')

            file.name = speks['filename']
        
        file.changed_at = datetime.datetime.today()
        file.save()

        if file.folder:
            file.folder.changed_at = date
            file.folder.save()
        else:
            file.repository.changed_at = date
            file.repository.save()
        
        speks = request.POST
        root = str(MEDIA_ROOT).replace('\\', '/')
        path_to_file = root + '/' + file.file.name

        with open(path_to_file, "w", encoding='utf-8') as f:
            f.write(speks['content'].replace('\n', ''))
            f.close()

        return redirect('file_fiew', pk)

def delete_file(request, pk):
    try:
        file = Document.objects.get(id=pk)
        if file.repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404

    date = datetime.datetime.today()

    if file.folder:
        file.folder.changed_at = date
        file.folder.save()
    else:
        file.repository.changed_at = date
        file.repository.save()

    file.delete()
    
    if file.folder:
        return redirect('folder_view', file.folder_id)
    else:
        return redirect('repository_view', file.repository_id)

def get_image(request, pk):
    try:
        file = Document.objects.get(id=pk)
        if file.repository.is_private and file.repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    root = str(MEDIA_ROOT).replace('\\', '/')
    print(root + file.file.name)
    
    response = HttpResponse(open(root + '/' + file.file.name, "rb"))
    response['Content-Type'] = 'image/png'
    response['X-Requested-With'] = 'XMLHttpRequest'
    return response

# Folder
def get_folder(request, pk):
    try:
        folder = Folder.objects.get(id=pk)
        if folder.owner.is_private and folder.owner.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    
    folder_files = folder.document_set.all()
    folder_folders = folder.folder_set.all()
    above = list(folder_files) + list(folder_folders)
    above.sort(key=lambda x: x.name)
    finally_above = []
    for i in above:
        time = datetime.datetime.today() - datetime.datetime(
                    i.changed_at.year, i.changed_at.month  ,i.changed_at.day, i.changed_at.hour, i.changed_at.minute)
        time = timedelta_to_dhms(time)

        if i.__class__.__name__ == 'Folder':
            finally_above.append([i, True, time])
        else:
            finally_above.append([i, False, i.name.split('.')[-1], time])
    
    
    data = {
        'folder': folder,
        'above': finally_above,
        'folder_tree': [folder.owner] + merge_list(folder_tree(folder))
    }
    return render(request, 'main/folder_view.html', data)

def create_folder(request):
    if request.user.is_authenticated and request.method == 'POST':
        speks = request.POST
        if speks['where_to'] == 'repository':
            try:
                repository = Repository.objects.get(id=int(speks.get('id')))
            except:
                raise Http404

            if request.user.profile != repository.owner:
                raise Http404

            try:
                repository.folder_set.get(name=speks.get('name'))
            except:
                pass
            else:
                data = {
                    'repository': repository,
                    'messeng': 'Папка с таким именем уже существует.'
                }
                return render(request, 'main/repository_settings.html', data)

            
            new_folder = Folder(
                owner = repository,
                name = speks.get('name'),
                created_at = datetime.datetime.today(),
                changed_at = datetime.datetime.today()
            )
            new_folder.save()
            return redirect('repository_view', repository.id)
        else:
            try:
                folder = Folder.objects.get(id=int(speks.get('id')))
            except:
                raise Http404

            if request.user.profile != folder.owner.owner:
                raise Http404

            try:
                folder.folder_set.get(name=speks.get('name'))
            except:
                pass
            else:
                data = {
                    'folder': folder,
                    'messeng': 'Папка с таким именем уже существует.'
                }
                return render(request, 'main/folder_settings.html', data)
            
            new_folder = Folder(
                owner = folder.owner,
                above_folder = folder,
                name = speks.get('name'),
                created_at = datetime.datetime.today(),
                changed_at = datetime.datetime.today()
            )
            new_folder.save()
            return redirect('folder_view', folder.id)
    else:
        raise Http404

def folder_settings(request, pk):
    try:
        folder = Folder.objects.get(id=pk)
        if folder.owner.owner != request.user.profile:
            raise Http404
    except:
        raise Http404

    if request.method == 'POST':
        speks = request.POST
        files = request.FILES
        print(files)
        
        
        if speks['name'] != folder.name:
            try:
                if folder.above_folder:
                    folder.above_folder.folder_set.get(name=speks['name'])
                else:
                    folder.owner.folder_set.get(name=speks['name'])
            except:
                pass
            else:
                data = {
                    'folder': folder,
                    'messeng': 'Папка с таким именем уже существует.'
                }
                return render(request, 'main/folder_settings.html', data)
            
            folder.name = speks['name']
            folder.changed_at = datetime.datetime.today()
            folder.save()
        if files:
            folder_files = folder.document_set.all()
            upload_files = []
            for i in files.getlist('files'):
                try:
                    file = folder_files.get(name=i.name)
                except:
                    upload_files.append(Document(
                        repository = folder.owner,
                        folder = folder,
                        name = i.name,
                        file = i,
                        created_at = datetime.datetime.today(),
                        changed_at = datetime.datetime.today()
                    ))
                else:
                    new_file = Document(
                        repository = file.repository,
                        folder = file.folder,
                        name = file.name,
                        file = i,
                        created_at = file.created_at,
                        changed_at = datetime.datetime.today()
                    )
                    file.delete()
                    new_file.save()
            
            Document.objects.bulk_create(upload_files)
        return redirect('folder_view', folder.id)
    else:
        data = {
            'folder': folder,
            'messeng': False
        }
        return render(request, 'main/folder_settings.html', data)

def delete_folder(request, pk):
    try:
        folder = Folder.objects.get(id=pk)
        if folder.owner.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    
    folder.delete()
    
    if folder.above_folder:
        return redirect('folder_view', folder.above_folder_id)
    else:
        return redirect('repository_view', folder.owner_id)

def download_folder(request, pk):
    try:
        folder = Folder.objects.get(id=pk)
        if folder.owner.is_private and folder.owner.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    
    folder_files = folder.document_set.all()
    folder_folders = folder.folder_set.all()
    root = str(MEDIA_ROOT).replace('\\', '/') + '/'
    path_to_repository = f'{root}user_{folder.owner.owner.owner_id}/repository_{folder.owner_id}/'
    
    os.chdir(path_to_repository)
    zipFile = zipfile.ZipFile(f'{folder.name}.zip', 'w', zipfile.ZIP_DEFLATED)
    
    
    for i in folder_files:
        filename = root + i.file.name
        zipFile.write(filename, i.name)
    
    if folder_folders:
        files_in_folders = iterate_in_folders(folder_folders)
        append_files_on_zip(files_in_folders, zipFile, root)

    zipFile.close()
    
    response = HttpResponse(open(path_to_repository + '/' + zipFile.filename, "rb"))
    response['Content-Type'] = f'application/zip; charset=utf-8'
    encoded_filename = urllib.parse.quote(zipFile.filename, encoding='utf-8')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_filename}"
    
    os.remove(path_to_repository + f'{folder.name}.zip')
    
    return response

# Repository
def get_repository(request, pk):
    try:
        repository = Repository.objects.get(id=pk)
        if repository.is_private and repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    
    repository_files = repository.document_set.filter(folder=None)
    repository_folders = repository.folder_set.filter(above_folder=None)
    above = list(repository_files) + list(repository_folders)
    above.sort(key=lambda x: x.name)
    
    finally_above = []
    
    for i in above:
        time = datetime.datetime.today() - datetime.datetime(
                    i.changed_at.year, i.changed_at.month  ,i.changed_at.day, i.changed_at.hour, i.changed_at.minute)
        time = timedelta_to_dhms(time)
        
        if i.__class__.__name__ == 'Folder':
            finally_above.append([i, True, time])
        else:
            finally_above.append([i, False, i.name.split('.')[-1], time])
    
    data = {
        'repository': repository,
        'above': finally_above,
    }
    return render(request, 'main/repository_view.html', data)

def create_repository(request):
    if request.user.is_authenticated and request.method == 'POST':
        speks = request.POST
        
        try:
            repositorys_set = request.user.profile.repository_set 
            repositorys_set.get(name=speks.get('name'))
        except:
            pass
        else:
            repositorys = []
            for i in repositorys_set.all():
                time = datetime.datetime.today() - datetime.datetime(
                                i.changed_at.year, i.changed_at.month  ,i.changed_at.day, i.changed_at.hour, i.changed_at.minute)
                time = timedelta_to_dhms(time)
                repositorys.append([i, time])
            data = {
                'profile': request.user.profile,
                'repositorys': repositorys,
                'messeng': 'Репозиторий с таким именем уже существует.'
            }
            return render(request, 'account/dashboard.html', data)
        
        repository = Repository(
            owner = request.user.profile,
            name = speks['name'],
            is_private = True if 'is_private' in speks == 'on' else False,
            created_at = datetime.datetime.today(),
            changed_at = datetime.datetime.today()
        )
        repository.save()

        return redirect('dashboard', request.user.profile.slug)
    else:
        raise Http404

def repository_settings(request, pk):
    try:
        repository = Repository.objects.get(id=pk)
        if repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404

    if request.method == 'POST':
        speks = request.POST
        files = request.FILES
        if speks['name'] != repository.name:
            try:
                repository.owner.repository_set.get(name=speks['name'])
            except:
                pass
            else:
                data = {
                    'repository': repository,
                    'messeng': 'Репозиторий с таким именем уже существует.'
                }
                return render(request, 'main/repository_settings.html', data)

            repository.name = speks['name']
            repository.changed_at = datetime.datetime.today()
            repository.save()
        if files:
            repository_files = repository.document_set.all()
            upload_files = []
            for i in files.getlist('files'):
                try:
                    file = repository_files.get(name=i.name)
                except:
                    upload_files.append(Document(
                        repository = repository,
                        name = i.name,
                        file = i,
                        created_at = datetime.datetime.today(),
                        changed_at = datetime.datetime.today()
                    ))
                else:
                    new_file = Document(
                        repository = file.repository,
                        name = file.name,
                        file = i,
                        created_at = file.created_at,
                        changed_at = datetime.datetime.today()
                    )
                    file.delete()
                    new_file.save()
            
            Document.objects.bulk_create(upload_files)
        return redirect('repository_view', repository.id)
    else:
        data = {
            'repository': repository,
            'messeng': False
        }
        return render(request, 'main/repository_settings.html', data)

def delete_repository(request, pk):
    try:
        repository = Repository.objects.get(id=pk)
        if repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404

    repository.delete()

    return redirect('dashboard', repository.owner.slug)

def download_repository(request, pk):
    try:
        repository = Repository.objects.get(id=pk)
        if repository.is_private and repository.owner != request.user.profile:
            raise Http404
    except:
        raise Http404
    
    repository_files = repository.document_set.filter(folder=None)
    repository_folders = repository.folder_set.filter(above_folder=None)
    root = str(MEDIA_ROOT).replace('\\', '/') + '/'
    path_to_repository = f'{root}user_{repository.owner.owner_id}/repository_{repository.id}/'
    os.chdir(path_to_repository)
    zipFile = zipfile.ZipFile(f'{repository.name}.zip', 'w', zipfile.ZIP_DEFLATED)
    
    for i in repository_files:
        filename = root + i.file.name
        zipFile.write(filename, i.name)
    
    if repository_folders:
        files_in_folders = iterate_in_folders(repository_folders)
        append_files_on_zip(files_in_folders, zipFile, root)

    zipFile.close()
    
    response = HttpResponse(open(path_to_repository + '/' + zipFile.filename, "rb"))
    response['Content-Type'] = f'application/zip; charset=utf-8'
    encoded_filename = urllib.parse.quote(zipFile.filename, encoding='utf-8')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_filename}"
    
    os.remove(path_to_repository + f'{repository.name}.zip')
    
    return response

# Additional
def iterate_in_folders(folders):
    if folders:
        files_in_folders = []
        for i in folders:
            files_in_folders.append({
                'name': i.name,
                'files': i.document_set.all(),
                'folders': iterate_in_folders(i.folder_set.all())
            })
        return files_in_folders
    else:
        return []

def folder_tree(folder):
    folders = []
    if folder.above_folder:
        folders += folder_tree(folder.above_folder), folder
        print(folder)
        return folders
    else:
        return folder

def append_files_on_zip(files_list, zip, root, zip_path=''):
        for i in files_list:
            if not i['files']:
                zip.write(str(MEDIA_ROOT).replace('\\', '/') + '/' + 'Пустая папка',zip_path + '/' + i['name'])
            for j in i['files']:
                zip.write(root + j.file.name,  zip_path + '/' + i['name'] + '/' + j.name + '/')
            
            
            append_files_on_zip(i['folders'], zip, root, zip_path + '/' + i['name'])

def merge_list(lis):
    if type(lis) == type([]):
        answer = []
        for i in lis:
            if type(i) == type([]):
                answer += merge_list(i)
            else:
                answer.append(i)
        return answer
    else:
        return [lis]

def timedelta_to_dhms(duration):
    # преобразование в дни, часы, минуты и секунды
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if days >= 365:
        time = f"{days // 365} years ago"
    elif days < 365 and days > 0:
        time = f"{days} days ago"
    else:
        if hours == 0:
            if minutes > 0:
                time = f"{minutes} minutes ago"
            else:
                time = "now"
        else:
            time = f"{hours} hours ago"
    
    return time