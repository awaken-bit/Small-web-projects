from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Profile(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.TextField(blank=True)
    groups = models.ManyToManyField('Group', blank=True)
    friends = models.ManyToManyField('Profile', blank=True)
    image = models.ImageField(blank=True, upload_to='images/profile/%Y/%m/%d', 
                            help_text='Аватар', verbose_name='Ссылка картинки')

    def __str__(self):
        return f'{self.owner.email} / {self.bio} / {self.owner.first_name}'

class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.owner.owner.email} / {self.post.text} / {self.text} / {self.date}'

class Like(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    
    def __str__(self):
        return f'{self.owner.owner.email} / {self.post.text}'

class Dizlike(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    
    def __str__(self):
        return f'{self.owner.owner.email} / {self.post.text}'

class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(blank=True, upload_to='images/blog/%Y/%m/%d', 
                            help_text='Картинка поста', verbose_name='Ссылка картинки')

    def __str__(self):
        return f'{self.owner.owner.email} / {self.text} / {self.id}'

class Group(models.Model):
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='group_admin')
    participants = models.ManyToManyField(Profile, blank=True)
    text = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images/group/%Y/%m/%d', 
                            help_text='Аватар группы', verbose_name='Ссылка картинки')
    def __str__(self):
        return f'{self.name} / {self.id}'

class Messange(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    addressee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='adress')
    text = models.TextField()
    pub_date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.sender.owner.first_name} / {self.addressee.owner.first_name} / {self.text}'

class MessangeGroup(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    addressee_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.sender.owner.email} / {self.addressee_group.name} / {self.text}'