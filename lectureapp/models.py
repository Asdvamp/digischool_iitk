from django.db import models
from backend_functions.universal_values import *


class ALL_LECTURES(models.Model):
    lecture_title = models.CharField(max_length=LECTURE_TITLE_LENGTH)
    yt_link_unique_id = models.URLField()
    # "course_id(10):lecture_series_number(2)"
    lecture_unique_id = models.CharField(max_length=LECTURE_UNIQUE_ID)
    course_mapping = models.ForeignKey(
        "courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)

    def __str__(self):
        return self.lecture_title

    class Meta:
        ordering = ['lecture_title']


class ALL_VIDEO(models.Model):
    connected_lecture = models.OneToOneField(
        ALL_LECTURES, on_delete=models.CASCADE)
    video_server_name = models.FileField(
        upload_to="videos/", null=True, verbose_name="")

    def __str__(self):
        return self.conneted_lecture

    class Meta:
        ordering = ['connected_lecture']
