from django.urls import reverse, resolve
from django.test import TestCase

# from ..views import boards
from ..views import BoardList
from ..models import Board

class BoardsTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.board = Board.objects.create(name = 'Django', description = 'Django board.')
        self.url = reverse('boards')

    def test_boards_view_status_code(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    # def test_boards_url_resolves_boards_view(self):
    #     view = resolve('/')
    #     self.assertEquals(view.func, boards)

    def test_boards_url_resolves_boards_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardList)

    def test_boards_view_contains_link_to_threads_page(self):
        self.response = self.client.get(self.url)
        board_threads_url = reverse('board_threads', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, f'href="{board_threads_url}"')
