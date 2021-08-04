from django.forms import ModelForm

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Comment, Thread
from ..views import CommentUpdate


class CommentUpdateTestCase(TestCase):
    '''
    Base test case to be used in all `CommentUpdate` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.thread = Thread.objects.create(title='Hello, world', board=self.board, creator=user)
        self.comment = Comment.objects.create(text='Lorem ipsum dolor sit amet', thread=self.thread, created_by=user)
        self.url = reverse('edit_comment', kwargs={
            'pk': self.board.pk,
            'thread_pk': self.thread.pk,
            'comment_pk': self.comment.pk
        })


class LoginRequiredCommentUpdateTests(CommentUpdateTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedCommentUpdateTests(CommentUpdateTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        '''
        A thread should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        '''
        self.assertEquals(self.response.status_code, 404)


class CommentUpdateTests(CommentUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/boards/1/threads/1/comments/1/edit/')
        self.assertEquals(view.func.view_class, CommentUpdate)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, text textarea
        '''
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulCommentUpdateTests(CommentUpdateTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'text': 'edited text'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        view_thread_url = reverse('view_thread', kwargs={'pk': self.board.pk, 'thread_pk': self.thread.pk})
        self.assertRedirects(self.response, view_thread_url)

    def test_comment_changed(self):
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.text, 'edited text')


class InvalidCommentUpdateTests(CommentUpdateTestCase):
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