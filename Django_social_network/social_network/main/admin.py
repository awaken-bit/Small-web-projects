from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Messange)
admin.site.register(MessangeGroup)
admin.site.register(Dizlike)
admin.site.register(Like)