from django.db import models

# Create your models here.
class Politicon(models.Model):
    euro = models.CharField(max_length=20)
    dollar = models.CharField(max_length=20)
    oil = models.CharField(max_length=20)

    def __str__(self):
        return f'{str(self.euro)} / {self.dollar} / {self.oil}'

class News(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    content = models.TextField()

    def __str__(self):
        return f'{self.title} / {self.subtitle}'