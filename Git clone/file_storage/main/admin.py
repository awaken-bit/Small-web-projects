from django.contrib import admin
from .models import *


admin.site.register(Profile)
admin.site.register(Repository)
admin.site.register(Document)
admin.site.register(Folder)