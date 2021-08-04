from django.urls import reverse, resolve
from django.test import TestCase

from ..views import ThreadList
from ..models import Board

class BoardThreadsTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.board = Board.objects.create(name = 'Django', description = 'Django board.')

    def test_board_threads_view_success_status_code(self):
        url = reverse('board_threads', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_threads_view_not_found_status_code(self):
        url = reverse('board_threads', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_threads_url_resolves_board_threads_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, ThreadList)

    def test_board_threads_view_contains_link_back_to_boards(self):
        board_threads_url = reverse('board_threads', kwargs={'pk': self.board.pk})
        boards_url = reverse('boards')

        response = self.client.get(board_threads_url)

        self.assertContains(response, f'href="{boards_url}"')

    def test_board_threads_view_contains_navigation_links(self):
        board_threads_url = reverse('board_threads', kwargs={'pk': self.board.pk})
        boards_url = reverse('boards')
        new_thread_url = reverse('new_thread', kwargs={'pk': self.board.pk})

        response = self.client.get(board_threads_url)

        self.assertContains(response, f'href="{boards_url}"')
        self.assertContains(response, f'href="{new_thread_url}"')
