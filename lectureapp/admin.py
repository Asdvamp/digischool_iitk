from django.contrib import admin
from .models import ALL_LECTURES, ALL_VIDEO


# Register your models here.
from . import models

admin.site.register(models.ALL_LECTURES)
admin.site.register(models.ALL_VIDEO)
