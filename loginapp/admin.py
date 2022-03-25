from django.contrib import admin
from .models import *

# Register your models here.
from . import models

admin.site.register(models.USER_SIGNUP_DATABASE)
admin.site.register(models.QUERY_DATABASE)
admin.site.register(models.TEACHER_CODE_MAPPING)
