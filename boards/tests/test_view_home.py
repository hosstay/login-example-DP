from django.urls import reverse, resolve
from django.test import TestCase

# from ..views import home
from ..views import BoardListView
from ..models import Board

class HomeTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.board = Board.objects.create(name = 'Django', description = 'Django board.')
        self.url = reverse('home')

    def test_home_view_status_code(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    # def test_home_url_resolves_home_view(self):
    #     view = resolve('/')
    #     self.assertEquals(view.func, home)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topics_page(self):
        self.response = self.client.get(self.url)
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
