from django.db import models
from backend_functions.universal_values import *

# Create your models here.


class ALL_FORUMS(models.Model):
    forum_title = models.CharField(max_length=FORUM_TITLE_LENGTH)
    # json format {"question" : "question content", "upvote counter"}
    forum_question = models.JSONField()
    forum_datetime = models.DateTimeField(auto_now_add=True)  # upload date.
    # "course_id(10):forum_series_number(2)"
    forum_unique_id = models.CharField(max_length=TEST_UNIQUE_ID)
    course_mapping = models.ForeignKey(
        "courseapp.AVAILABLE_COURSES", on_delete=models.CASCADE)
    # json format {"answer1": "answer content", "date_answer": "datetime string" , "user" : "loginapp.USER_SIGNUPUP_DATABASE.id", "upvotecounter": value (negative means more downvotes)}
    forum_answers = models.JSONField()

    def __str__(self):
        return self.forum_title

    class Meta:
        ordering = ['forum_datetime']
