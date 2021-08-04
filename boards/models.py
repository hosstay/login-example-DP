from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_comments_count(self):
        return Comment.objects.filter(thread__board=self).count()

    def get_last_comment(self):
        return Comment.objects.filter(thread__board=self).order_by('-created_at').first()


class Thread(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_comment_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='threads')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_page_count(self):
        count = self.comments.count()
        pages = count / 2
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_comments(self):
        return self.comments.order_by('-created_at')[:10]


class Comment(models.Model):
    text = models.TextField(max_length=4000)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments', null=True)
    is_master = models.BooleanField(default=False)
    parent = models.IntegerField(default=-1)
    children = ArrayField(models.PositiveIntegerField(), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        truncated_text = Truncator(self.text)
        return truncated_text.chars(30)

    def get_text_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))