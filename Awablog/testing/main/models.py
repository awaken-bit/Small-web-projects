from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    user_main = models.ManyToManyField(User)

    def __str__(self):
        return str([i.username for i in self.user_main.all()][0])

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    author_blog = models.ManyToManyField(Author)

    def __str__(self):
        return self.name


class User_vie(models.Model):
    user_main = models.ManyToManyField(User)

    def __str__(self):
        return str([i.username for i in self.user_main.all()][0])

class Entry(models.Model):
    blog = models.ManyToManyField(Blog)      # Это число
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    authors = models.ManyToManyField(Author)     # Это число


    def __str__(self):
        return self.headline

class Likeq(models.Model):
    author = models.ManyToManyField(User)
    post = models.ManyToManyField(Entry)
    def __str__(self):
        return str(list(self.post.all()) + list(self.author.all()))
class Dizlikeq(models.Model):
    author = models.ManyToManyField(User)
    post = models.ManyToManyField(Entry)
    def __str__(self):
        return str(list(self.post.all()) + list(self.author.all()))