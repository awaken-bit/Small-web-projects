from django.db import models

# Create your models here.
class Artiles(models.Model):
    title = models.CharField('Название',max_length=70)
    who = models.IntegerField(default=0)
    text = models.TextField('Статья')


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return '/news/'
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'