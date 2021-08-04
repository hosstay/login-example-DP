from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import CommentForm
from ..models import Board, Comment, Thread
from ..views import NewParentComment

class NewParentCommentTestCase(TestCase):
    '''
    Base test case to be used in all `new_parent_comment` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.thread = Thread.objects.create(title='Hello, world', board=self.board, creator=user)
        Comment.objects.create(text='Lorem ipsum dolor sit amet', thread=self.thread, created_by=user)
        self.url = reverse('new_parent_comment', kwargs={'pk': self.board.pk, 'thread_pk': self.thread.pk})

class LoginRequiredNewParentCommentTests(NewParentCommentTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')

class NewParentCommentTests(NewParentCommentTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/threads/1/new_parent_comment/')
        self.assertEquals(view.func.view_class, NewParentComment)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CommentForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, text textarea
        '''
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulNewParentCommentTests(NewParentCommentTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'text': 'hello, world!'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        url = reverse('view_thread', kwargs={'pk': self.board.pk, 'thread_pk': self.thread.pk})
        view_thread_url = f'{url}?page=1#22'
        self.assertRedirects(self.response, view_thread_url)

    def test_reply_created(self):
        '''
        The total comment count should be 2
        The one created in the `NewParentCommentTestCase` setUp
        and another created by the post data in this class
        '''
        self.assertEquals(Comment.objects.count(), 2)

class InvalidNewParentCommentTests(NewParentCommentTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `new_parent_comment` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)