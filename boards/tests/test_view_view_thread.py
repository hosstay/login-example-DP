from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Comment, Thread
from ..views import CommentList

class ViewThreadTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        thread = Thread.objects.create(title='Hello, world', board=board, creator=user)
        Comment.objects.create(text='Lorem ipsum dolor sit amet', thread=thread, created_by=user)
        url = reverse('view_thread', kwargs={'pk': board.pk, 'thread_pk': thread.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/threads/1/')
        self.assertEquals(view.func.view_class, CommentList)