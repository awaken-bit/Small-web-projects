from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from file_storage.settings import MEDIA_ROOT

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            owner = instance,
            slug = hash(str(instance.id))
        )
        profile.save()




# documents/%Y/%m/%d/
def user_directory_path(instance, filename):
    if instance.folder:
        # folder_documents = instance.folder.document_set.all()
        # folder_documents[0].file.name.split('/')[-2] if folder_documents else instance.folder.name,
        return 'user_{0}/repository_{1}/{2}/{3}'.format(instance.repository.owner.owner_id,
                                                        instance.repository_id,
                                                        instance.folder.name,
                                                        filename)
    else:
        return 'user_{0}/repository_{1}/{2}'.format(instance.repository.owner.owner_id, instance.repository_id, filename)

def profile_avatars(instance, filename):
    return f'images/profiles/{filename}'

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    favorites = models.ManyToManyField('Profile', blank=True)
    image = models.ImageField(blank=True, upload_to=profile_avatars, 
                            help_text='Аватар', verbose_name='Ссылка картинки')
    slug = models.SlugField()
    
    def __str__(self):
        return self.owner.username

class Repository(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_private = models.BooleanField()
    created_at = models.DateTimeField()
    changed_at = models.DateTimeField()
    

    def __str__(self):
        return self.name

class Document(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
    created_at = models.DateTimeField()
    changed_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.file.name} / {self.repository.name} / {self.id}'

@receiver(post_delete, sender=Document)
def delete_document(sender, instance, **kwargs):
    if instance.file:
        root = str(MEDIA_ROOT).replace('\\', '/') + '/'
        filename = instance.file.name
        folder = root + '/'.join(filename.split('/')[:-1])

        instance.file.delete()
        instance.delete()
        try:
            if not os.listdir(folder):
                os.rmdir(folder)
        except:
            pass

class Folder(models.Model):
    owner = models.ForeignKey(Repository, on_delete=models.CASCADE)
    above_folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    changed_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.name} / {self.id}'

@receiver(post_save, sender=Folder)
def folder_save(sender, instance, **kwargs):
    date = datetime.today()

    if instance.above_folder:
        instance.above_folder.changed_at = date
        instance.above_folder.save()
    else:
        instance.owner.changed_at = date
        instance.owner.save()

@receiver(post_delete, sender=Folder)
def delete_folder(sender, instance, **kwargs):
    root = str(MEDIA_ROOT).replace('\\', '/') + '/'
    for i in instance.document_set.all():
        filename = i.file.name
        i.delete()
        
    
    date = datetime.today()

    if instance.above_folder:
        instance.above_folder.changed_at = date
        instance.above_folder.save()
    else:
        instance.owner.changed_at = date
        instance.owner.save()


