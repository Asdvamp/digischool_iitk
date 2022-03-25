from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.ALL_LECTURES)
admin.site.register(models.ALL_VIDEO)
