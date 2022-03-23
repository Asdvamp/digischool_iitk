from django.contrib import admin

from .models import CLASS_COURSES_MAPPING, AVAILABLE_COURSES

admin.site.register(CLASS_COURSES_MAPPING)
admin.site.register(AVAILABLE_COURSES)
