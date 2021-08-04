from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import new_thread
from ..models import Board, Thread, Post
from ..forms import NewThreadForm

class LoginRequiredNewThreadTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_thread', kwargs={'pk': self.board.pk})

    def setUp(self):
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class NewThreadTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.board = Board.objects.create(name = 'Django', description = 'Django board.')
        self.user = User.objects.create_user(username = 'john', email = 'john@doe.com', password = '123')
    
    def setUp(self):
        self.client.login(username = 'john', email = 'john@doe.com', password = '123')

    def test_new_thread_view_success_status_code(self):
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_thread_view_not_found_status_code(self):
        url = reverse('new_thread', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_thread_url_resolves_new_thread_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_thread)

    def test_new_thread_view_contains_link_back_to_board_threads_view(self):
        new_thread_url = reverse('new_thread', kwargs={'pk': self.board.pk})
        board_threads_url = reverse('board_threads', kwargs={'pk': self.board.pk})
        response = self.client.get(new_thread_url)
        self.assertContains(response, f'href="{board_threads_url}"')

    def test_csrf(self):
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_thread_valid_post_data(self):
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        data = {
            'title': 'Test title',
            'text': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Thread.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewThreadForm)

    def test_new_thread_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_thread_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_thread', kwargs={'pk': self.board.pk})
        data = {
            'title': '',
            'text': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Thread.objects.exists())
        self.assertFalse(Post.objects.exists())